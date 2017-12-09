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

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-25"


class ConfigurationParameter:
    def __init__(self, names=None, methods=None):
        if methods is None:
            methods = {}
        if names is None:
            names = {}
        self.names = names
        self.methods = methods
        self.condition_state = {}
        self.draft = None
        self.current_method_name = None
        self.skip_indent_level = -1
        self.is_if_statement = None
        self.stop = -1
