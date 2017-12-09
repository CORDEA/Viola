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

from src.impl.enum.type import *
from src.impl.model.definition import *

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2016-01-04"


class Out:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    def Eco(self, fs, sc=None):
        if isinstance(fs, Definition):
            obj = self.handler.get_reserved_obj(fs.parameter, self.cp)
            fs = self.handler.exec_reserved_method(obj, self.cp)[1]
        else:
            fs = self.handler.expression_from_tuple(fs, self.cp.names)
        if fs.value_type == Type.list:
            print_list = [str([rs.value for rs in fs.value])]
        else:
            print_list = [fs.value]
        if sc:
            sc = self.handler.expression_from_tuple(sc, self.cp.names)
            if sc.value_type == Type.list:
                print_list.append(str([rs.value for rs in sc.value]))
            else:
                print_list.append(sc.value)
        print " ".join([str(k) for k in print_list])
