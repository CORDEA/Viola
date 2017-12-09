#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2015-2016 Yoshihiro Tanaka
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

import v_lex
from enum.constants import *
from enum.method_mode import *
from enum.type import *
from model.condition_state import *
from model.configuration_parameter import *
from model.definition import *
from model.method import *
from model.method_return import *
from model.value import *
from src.impl.error import UndefinedError, IllegalMethodError, WrongSyntaxError, UnknownOperatorError, \
    AlreadyDefinedError
from src.impl.method_handler import MethodHandler
from src.impl.reserved_method_caller import ReservedMethodCaller

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-26"

handler = MethodHandler()


def get_value_from_obj(cp, p):
    param = p.parameter
    if isinstance(param[1], Definition):
        if len(param[1].parameter) == 1:
            name = param[1].parameter[0]
        else:
            name = param[1].parameter[1]
        if ReservedMethodCaller.is_reserved_method(name):
            obj = handler.get_reserved_obj(param[1].parameter, cp)
            cp.names[param[0].value] = handler.exec_reserved_method(obj, cp)[1]
        else:
            p = get_exec_method_obj(param[1].parameter, cp.methods)
            mr = execute_method(p, cp.names, cp.methods)
            if mr and mr.ret and mr.ret.value in mr.names:
                cp.names[param[0].value] = mr.names[mr.ret.value]
    else:
        cp.names[param[0].value] = handler.expression_from_tuple(param[1], cp.names)


def get_method_definition(cp, p):
    cp.current_method_name = p[1]
    param = cp.draft.parameter
    if len(p) == 2:
        if p[1] in cp.methods:
            raise AlreadyDefinedError(p[1])
        else:
            if p[0].value in cp.names:
                raise AlreadyDefinedError(p[0])
            else:
                if param[0].value_type != Type.discard:
                    cp.names[param[0].value] = handler.expression_from_tuple(param[1], cp.names)
                method = Method(param[0], p[1], (p[0],), cp.draft.annotation)
    else:
        if p[2] in cp.methods:
            raise AlreadyDefinedError(p[2])
        else:
            if param[0].value_type != Type.discard:
                cp.names[param[0].value] = handler.expression_from_tuple(param[1], cp.names)
            method = Method(param[0], p[1], (p[0], p[2]), cp.draft.annotation)
    return Definition(Constants.def_method, method)


def __check_condition(p, names):
    if len(p) == 1:
        return p[0].value
    else:
        chk = [p[0], p[2]]
        for i in range(len(chk)):
            if isinstance(chk[i], Value):
                if chk[i].value_type == Type.var:
                    if chk[i].value in names:
                        chk[i] = names[chk[i].value]
                    else:
                        raise UndefinedError(chk[i].value)
            else:
                chk[i] = handler.expression_from_tuple(chk[i], names)
            chk[i] = chk[i].value
        if p[1] == v_lex.t_EEQUALS:
            return chk[0] == chk[1]
        elif p[1] == v_lex.t_ENEQUALS:
            return chk[0] != chk[1]
        else:
            raise UnknownOperatorError(p[1])


def question_from_tuple(p, cp):
    cp.is_if_statement = True
    param = p.parameter
    if len(param) == 1:
        if (p.indent_level + 1) in cp.condition_state:
            cp.condition_state[p.indent_level + 1].if_eval = not cp.condition_state[p.indent_level + 1].pass_first_if
    else:
        flag = __check_condition(param[1], cp.names)
        if param[0] == ">":
            cp.condition_state[p.indent_level + 1] = ConditionState(flag, flag)
        else:
            if (p.indent_level + 1) in cp.condition_state:
                if cp.condition_state[p.indent_level + 1].pass_first_if:
                    cp.condition_state[p.indent_level + 1].if_eval = False
                else:
                    cp.condition_state[p.indent_level + 1] = ConditionState(flag, flag)
            else:
                raise WrongSyntaxError(p)


def __def_var_assign(p, cp, ret):
    param = p.parameter
    if param[0].value == ret.value:
        if p.indent_level > 0:
            cp.stop = p.indent_level
    if param[1]:
        get_value_from_obj(cp, p)
    else:
        cp.names[param[0].value] = None


def execute_method(p, names, methods):
    param = p.parameter
    method = param[0]
    passes = method.passes
    if passes:
        inside_params = __get_method_config_parameters(names, methods, p, True)
        mode = MethodMode.start
        while True:
            if (mode == MethodMode.recursive and mode != MethodMode.stop) or mode == MethodMode.start:
                for i in passes:
                    m = __eval_per_line(inside_params, i, method.ret)
                    if type(m) == tuple:
                        if len(m) == 2:
                            mode, param = m
                            p = get_exec_method_obj(param, inside_params.methods)
                            inside_params = __get_method_config_parameters(
                                inside_params.names, inside_params.methods, p)
                    else:
                        mode = m
            else:
                break

        if method.ret:
            if method.ret.value_type != Type.discard and method.ret.value in inside_params.names:
                return MethodReturn(method.ret, inside_params.names)
    else:
        raise IllegalMethodError(method.name)


def __get_method_config_parameters(names, methods, p, deep=False):
    param = p.parameter
    method = param[0]

    dic = copy.deepcopy(names) if deep else names
    if len(param) == 2:
        dic[method.arg[0].value] = handler.expression_from_tuple(param[1], names)
    else:
        p1 = handler.expression_from_tuple(param[1], names)
        p2 = handler.expression_from_tuple(param[2], names)
        dic[method.arg[0].value] = p1
        dic[method.arg[1].value] = p2
    return ConfigurationParameter(dic, copy.deepcopy(methods) if deep else methods)


def get_exec_method_obj(p, methods):
    if p[1] in methods:
        if len(p) == 2:
            method = Definition(Constants.exec_method, (methods[p[1]], p[0]))
        else:
            method = Definition(Constants.exec_method, (methods[p[1]], p[0], p[2]))
    else:
        raise UndefinedError(p[1])

    return method


def __eval_per_line(inside_cp, p, ret):
    get_from = p.get_from
    if inside_cp.stop != -1 and inside_cp.stop <= p.indent_level + 1:
        return MethodMode.stop
    if p.get_from != Constants.condition and p.get_from != Constants.def_method:
        if (p.indent_level + 1) in inside_cp.condition_state:
            del inside_cp.condition_state[p.indent_level + 1]
        if p.indent_level in inside_cp.condition_state:
            if not inside_cp.condition_state[p.indent_level].if_eval:
                return
    if get_from == Constants.def_method:
        raise UndefinedError(p.parameter)
    elif get_from == Constants.condition:
        question_from_tuple(p, inside_cp)
    elif get_from == Constants.def_var:
        __def_var_assign(p, inside_cp, ret)
    elif get_from == Constants.def_var_assign:
        __def_var_assign(p, inside_cp, ret)
    elif get_from == Constants.def_return:
        pass
    elif get_from == Constants.exec_method:
        param = p.parameter
        if ReservedMethodCaller.is_reserved_method(param[1]):
            obj = handler.get_reserved_obj(param, inside_cp)
            handler.exec_reserved_method(obj, inside_cp)
            return
        else:
            return MethodMode.recursive, param
