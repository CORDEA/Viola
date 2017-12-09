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

from src.impl.enum.reserved_name import *
from src.impl.enum.type import *
from src.impl.model.value import *

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2016-01-04"


class List:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    def Init(self):
        return ReservedName.Init, Value(Type.list, [])

    def Add(self, fs, sc):
        sc = self.handler.expression_from_tuple(sc, self.cp.names)
        if fs.value in self.cp.names:
            self.cp.names[fs.value].value.append(sc)
        else:
            self.cp.names[fs.value] = Value(Type.list, [sc])
        return ReservedName.List, (fs.value, self.cp.names[fs.value])

    def Get(self, fs, sc):
        assert fs.value in self.cp.names and sc.value_type == Type.int
        return ReservedName.Get, Value(sc.value_type, self.cp.names[fs.value].value[sc.value].value)

    def Pop(self, fs, sc):
        assert fs.value in self.cp.names and sc.value_type == Type.int
        lst = self.cp.names[fs.value].value
        lst.pop(sc.value)
        self.cp.names[fs.value] = Value(Type.list, lst)

    def Contains(self, fs, sc):
        assert fs.value in self.cp.names
        lst = [r.value for r in self.cp.names[fs.value].value]
        if sc.value in lst:
            return ReservedName.Contains, Value(Type.bool, True)
        return ReservedName.Contains, Value(Type.bool, False)

    def Length(self, fs):
        assert fs.value in self.cp.names and type(self.cp.names[fs.value].value) == list
        return ReservedName.Length, Value(Type.int, len(self.cp.names[fs.value].value))
