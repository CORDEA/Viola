#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2017 Yoshihiro Tanaka
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

import unittest

from src.impl.method_handler import MethodHandler
from src.impl.model.configuration_parameter import ConfigurationParameter
from src.impl.reserved.file import File
from src.impl.reserved.list import List
from src.impl.reserved.out import Out
from src.impl.reserved_method_caller import ReservedMethodCaller

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2017-12-11"


class TestReservedMethodCaller(unittest.TestCase):

    def test_is_reserved_method(self):
        actual = ReservedMethodCaller.is_reserved_method("Eco")
        self.assertEqual(True, actual)

        actual = ReservedMethodCaller.is_reserved_method("System'RunCmd")
        self.assertEqual(True, actual)

        actual = ReservedMethodCaller.is_reserved_method("List'Add")
        self.assertEqual(True, actual)

        actual = ReservedMethodCaller.is_reserved_method("List'Pop")
        self.assertEqual(True, actual)

        actual = ReservedMethodCaller.is_reserved_method("Test'Assert")
        self.assertEqual(True, actual)

    def test_core(self):
        caller = ReservedMethodCaller(ConfigurationParameter(), MethodHandler())
        actual = caller.core("Eco", [""])
        self.assertEqual(type(Out), type(actual.cls))
        self.assertEqual(1, len(actual.args))
        self.assertEqual("Eco", actual.method.__name__)

        caller = ReservedMethodCaller(ConfigurationParameter(), MethodHandler())
        actual = caller.core("List'Init", [])
        self.assertEqual(type(List), type(actual.cls))
        self.assertEqual(0, len(actual.args))
        self.assertEqual("Init", actual.method.__name__)

        caller = ReservedMethodCaller(ConfigurationParameter(), MethodHandler())
        actual = caller.core("File'OpenWrite", ["", ""])
        self.assertEqual(type(File), type(actual.cls))
        self.assertEqual(2, len(actual.args))
        self.assertEqual("OpenWrite", actual.method.__name__)


if __name__ == "__main__":
    unittest.main()
