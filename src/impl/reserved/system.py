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

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2016-08-26"

import commands

from src.impl.enum.reserved_name import ReservedName
from src.impl.enum.type import Type
from src.impl.model.value import Value


class System:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    def RunCmd(self, fs):
        exe = None
        if fs.value_type == Type.var:
            exe = self.cp.names[fs.value].value
        if fs.value_type == Type.string:
            exe = fs.value
        out = commands.getoutput(exe)
        return ReservedName.RunCmd, Value(Type.string, out)
