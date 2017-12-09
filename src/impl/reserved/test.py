#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2016 Yoshihiro Tanaka
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
__date__ = "2016-08-23"


class Test:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    def Assert(self, fs, sc):
        assert self.__get_value(fs) == self.__get_value(sc)

    def __get_value(self, obj):
        if isinstance(obj, Definition):
            obj = self.handler.get_reserved_obj(obj.parameter, self.cp)
            val = self.handler.exec_reserved_method(obj, self.cp)[1]
        else:
            val = self.handler.expression_from_tuple(obj, self.cp.names)
        if val.value_type == Type.list:
            return [rs.value for rs in val.value]
        else:
            return val.value
