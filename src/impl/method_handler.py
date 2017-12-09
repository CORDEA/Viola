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

import re
import math

from src.impl.enum.type import Type
from src.impl.error import UndefinedError, IllegalMethodError
from src.impl.model.definition import Definition
from src.impl.model.value import Value
from src.impl.reserved_method_caller import ReservedMethodCaller

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-21"


class MethodHandler:
    def __init__(self):
        pass

    def expression_from_tuple(self, p, names):
        is_float = False
        if type(p) == tuple:
            if len(p) == 1:
                return self.expression_from_tuple(p[0], names)
            p = list(p)
            for i in range(len(p)):
                if isinstance(p[i], Value):
                    if p[i].value_type == Type.var:
                        if p[i].value in names:
                            p[i] = names[p[i].value]
                        else:
                            p[i] = None
            for i in range(len(p)):
                if type(p[i]) == float or (isinstance(p[i], Value) and p[i].value_type == Type.float):
                    is_float = True

            exp = " ".join([str(r.value) if isinstance(r, Value) else str(r) for r in p])
            if is_float:
                exp = re.sub(r'//[ \t]*(\d+\.\d+)', r'math.sqrt(\1)', exp)
                return Value(Type.float, eval(exp))
            else:
                exp = re.sub(r'//[ \t]*(\d+)', r'int(math.ceil(math.sqrt(\1)))', exp)
                return Value(Type.int, eval(exp))
        else:
            if isinstance(p, Value):
                if p.value_type == Type.var:
                    if p.value in names:
                        return self.expression_from_tuple(names[p.value], names)
                    else:
                        raise UndefinedError(p.value)
            elif isinstance(p, Definition):
                print "Unimplemented"
            return p

    def exec_reserved_method(self, rm, cp):
        res = ReservedMethodCaller(cp, self)
        return res.fire(rm)

    def get_reserved_obj(self, pr, cp):
        res = ReservedMethodCaller(cp, self)
        if len(pr) == 1:
            method = pr[0]
            args = ()
        elif len(pr) == 2:
            method = pr[1]
            args = (pr[0],)
        elif len(pr) == 3:
            method = pr[1]
            args = (pr[0], pr[2])
        else:
            raise IllegalMethodError(pr[1])
        return res.core(method, args)
