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

import sys
import warnings

import ply.yacc as yacc

from src.impl import v_lex
from src.impl.enum.constants import Constants
from src.impl.enum.reserved_name import *
from src.impl.enum.type import Type
from src.impl.method_handler import MethodHandler
from src.impl.model.configuration_parameter import ConfigurationParameter
from src.impl.model.definition import Definition
from src.impl.model.draft import *
from src.impl.model.value import Value
from src.impl.reserved_method_caller import ReservedMethodCaller
from src.impl.viola import get_value_from_obj, get_method_definition, get_exec_method_obj, execute_method, \
    question_from_tuple

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-20"

tokens = v_lex.tokens

precedence = (
    ('left', 'BRACKET_RIGHT', 'BRACKET_LEFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULUS'),
    ('left', 'POWER', 'SQRT'),
    ('left', 'METHOD')
)

parameter = ConfigurationParameter()
handler = MethodHandler()


def p_statements(p):
    '''statements : line NL statements
    | empty NL statements
    | INDENT NL statements
    | line empty
    | empty'''
    if len(p) == 3:
        p[0] = p[2]


def p_line(p):
    'line : statement'
    p[0] = __statement_method(p[1])


def p_statement_def(p):
    '''statement : VAR
    | INDENT VAR'''
    il = 0
    if len(p) == 2:
        m = (p[1], None)
    else:
        il = p[1]
        m = (p[2], None)
    p[0] = Definition(Constants.def_var, m, il)


def p_statement_annot(p):
    '''statement : ANNOT'''
    p[0] = Definition(Constants.def_annotation, p[1])


def deindent_initialize():
    if parameter.is_if_statement:
        parameter.is_if_statement = False
        return
    parameter.skip_indent_level = -1


def p_statement_assign(p):
    '''statement : VAR EQUALS expression
    | INDENT VAR EQUALS expression
    | VAR EQUALS exec
    | INDENT VAR EQUALS exec'''
    il = 0
    if len(p) == 4:
        m = (p[1], p[3])
    else:
        m = (p[2], p[4])
        il = p[1]
    p[0] = Definition(Constants.def_var_assign, m, il)


def p_statement_return_dis(p):
    '''statement : VAR IN
    | INDENT VAR IN'''
    if len(p) == 3:
        p[0] = Definition(Constants.def_return, (p[1],))
    else:
        p[0] = Definition(Constants.def_return, (p[2],), p[1])


def p_statement_return(p):
    '''statement : VAR EQUALS expression IN
    | INDENT VAR EQUALS expression IN'''
    if len(p) == 5:
        p[0] = Definition(Constants.def_return, (p[1], p[3]))
    else:
        p[0] = Definition(Constants.def_return, (p[2], p[4]), p[1])


def p_statement_method(p):
    '''statement : question
    | INDENT question
    | exec
    | INDENT exec'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        pas = p[2]
        pas.add_indent_level(p[1])
        p[0] = pas


def __statement_method(p):
    get_from = p.get_from
    if parameter.stop != -1 and parameter.stop <= p.indent_level + 1:
        return
    if p.get_from != Constants.condition and p.get_from != Constants.def_method:
        if p.indent_level == 0:
            parameter.current_method_name = None
        if (p.indent_level + 1) in parameter.condition_state:
            del parameter.condition_state[p.indent_level + 1]
            deindent_initialize()
        for key in parameter.condition_state.keys():
            if p.indent_level >= key:
                if not parameter.condition_state[key].if_eval:
                    return
    if parameter.current_method_name:
        if p.get_from != Constants.def_method:
            parameter.methods[parameter.current_method_name].add_pass(p)
            return
    if get_from == Constants.condition:
        question_from_tuple(p, parameter)
    elif get_from == Constants.def_method:
        if p.indent_level not in parameter.condition_state or parameter.condition_state[p.indent_level].if_eval:
            parameter.methods[p.parameter.name] = p.parameter
            parameter.draft = None
    elif get_from == Constants.def_var:
        parameter.names[p.parameter[0].value] = None
    elif get_from == Constants.def_annotation:
        parameter.draft = Draft()
        parameter.draft.annotation = p.parameter
    elif get_from == Constants.def_var_assign:
        get_value_from_obj(parameter, p)
    elif get_from == Constants.def_return:
        parameter.draft = Draft(p.parameter)
    elif get_from == Constants.exec_method:
        param = p.parameter
        if len(param) > 1 and ReservedMethodCaller.is_reserved_method(param[1]):
            obj = handler.get_reserved_obj(param, parameter)
            if p.indent_level not in parameter.condition_state or parameter.condition_state[p.indent_level].if_eval:
                ex = handler.exec_reserved_method(obj, parameter)
                if ex:
                    if ex[0] == ReservedName.List:
                        parameter.names[ex[1][0]] = ex[1][1]
                    elif ex[0] == ReservedName.Get:
                        pass
            return
        if parameter.draft:
            if len(param) == 2:
                if isinstance(param[0], Value):
                    if param[0].value_type == Type.var:
                        p = get_method_definition(parameter, param)
            else:
                if isinstance(param[0], Value) and isinstance(param[2], Value):
                    if param[0].value_type == Type.var and param[2].value_type == Type.var:
                        p = get_method_definition(parameter, param)
            parameter.draft = None

            if p.get_from == Constants.def_method:
                if p.indent_level not in parameter.condition_state or parameter.condition_state[p.indent_level].if_eval:
                    parameter.methods[p.parameter.name] = p.parameter
            else:
                raise ValueError()
        else:
            p = get_exec_method_obj(param, parameter.methods)
            mr = execute_method(p, parameter.names, parameter.methods)
            if mr and mr.ret and mr.ret.value in mr.names:
                warnings.warn("deprecated", DeprecationWarning)
            parameter.draft = None


def p_exec_method_with_bracket(p):
    '''exec : BRACKET_LEFT METHOD BRACKET_RIGHT
    | BRACKET_LEFT reserved_pattern METHOD BRACKET_RIGHT
    | BRACKET_LEFT reserved_pattern METHOD reserved_pattern BRACKET_RIGHT'''
    p[0] = Definition(Constants.exec_method, p[2:(len(p) - 1)])


def p_exec_method(p):
    '''exec : METHOD
    | reserved_pattern METHOD
    | reserved_pattern METHOD reserved_pattern'''
    p[0] = Definition(Constants.exec_method, p[1:])


def p_reserved_pattern(p):
    '''reserved_pattern : expression
    | exec'''
    p[0] = p[1]


def p_question(p):
    '''question : IF eval
    | ELIF eval
    | ELIF'''
    if len(p) == 3:
        p[0] = Definition(Constants.condition, (p[1], p[2]))
    else:
        p[0] = Definition(Constants.condition, (p[1],))


def p_eval(p):
    '''eval : exec operator
    | expression operator
    | exec operator exec
    | expression operator expression
    | TRUE
    | FALSE'''
    p[0] = p[1:]


def p_operators_for_eval(p):
    '''operator : EEQUALS
    | ENEQUALS'''
    p[0] = p[1]


def p_expression_type(p):
    'expression : type'
    p[0] = p[1]


def p_type(p):
    '''type : VAR
    | NUMBER
    | STRING
    | bool
    | NONE'''
    p[0] = p[1]


def p_bool(p):
    '''bool : TRUE
    | FALSE'''
    p[0] = p[1]


def p_array(p):
    '''array : expression ARRAY expression'''
    p[0] = Value(Type.list, [Value(Type.int, r) for r in range(p[1].value, p[3].value)])


def p_expression_with_bracket(p):
    '''expression : BRACKET_LEFT expression BRACKET_RIGHT'''
    lst = p[1:]
    chk_list = [type(r) == tuple for r in lst]
    if True in chk_list:
        res = []
        [res.extend(r) if type(r) == tuple else res.append(r) for r in lst]
        lst = res
    p[0] = tuple(lst)


def p_expression_binop(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | expression MODULUS expression
                | expression POWER expression
                | array
                | SQRT expression'''
    lst = p[1:]
    chk_list = [type(r) == tuple for r in lst]
    if True in chk_list:
        res = []
        [res.extend(r) if type(r) == tuple else res.append(r) for r in lst]
        lst = res
    p[0] = tuple(lst)


def p_empty(p):
    'empty : '
    pass


def p_error(p):
    print("Syntax error at '%s'" % p.value.value)


class Viola:
    def __init__(self):
        self.parser = yacc.yacc(debug=0)

    def run(self, c=None):
        if not c:
            argv = sys.argv
            if len(argv) > 1:
                with open(argv[1]) as f:
                    c = f.read()

        if c:
            self.parser.parse(c)


if __name__ == '__main__':
    s = Viola()
    s.run()
