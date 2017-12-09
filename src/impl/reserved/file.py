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
from src.impl.error import *
from src.impl.model.value import *

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2016-01-06"


class File:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    def Read(self, fs):
        lines = []
        if isinstance(fs, Value):
            with open(fs.value) as f:
                lines = [Value(Type.string, r) for r in f.readlines()]
        return ReservedName.Read, Value(Type.list, lines)

    def OpenWrite(self, fs, sc):
        if isinstance(fs, Value):
            with open(fs.value, 'aw') as f:
                f.write(sc.value)

    def Write(self, fs, sc):
        if isinstance(fs, Value):
            self.__get_file_obj(fs).write(sc.value)

    def Open(self, fs, sc=None):
        f = None
        if isinstance(fs, Value):
            if sc:
                f = open(fs.value, sc.value)
            else:
                f = open(fs.value)
            return ReservedName.Open, Value(Type.file, f)
        raise NoneError(f)

    def Close(self, fs):
        if isinstance(fs, Value):
            self.__get_file_obj(fs).close()

    def __get_file_obj(self, fs):
        if fs.value in self.cp.names:
            return self.cp.names[fs.value].value
        raise UndefinedError(fs.value)
