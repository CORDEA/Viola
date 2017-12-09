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
__date__ = "2016-08-23"


class Definition:
    def __init__(self, get_from, parameter, indent_level=0):
        self.get_from = get_from
        self.parameter = parameter
        self.indent_level = indent_level

    def add_indent_level(self, indent_level):
        self.indent_level = indent_level
