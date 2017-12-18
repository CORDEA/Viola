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

from src.impl.enum.type import Type
from src.impl.method_handler import MethodHandler
from src.impl.model.configuration_parameter import ConfigurationParameter
from src.impl.model.value import Value
from src.impl.reserved.test import Test

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2017-12-18"


class TestTest(unittest.TestCase):

    def test_Assert(self):
        test = Test(ConfigurationParameter(), MethodHandler())
        test.Assert(Value(Type.string, "1"), Value(Type.string, "1"))

        test.Assert(Value(Type.int, 1), Value(Type.int, 1))

        test.Assert(Value(Type.float, 1.1), Value(Type.float, 1.1))

        test.Assert(
            Value(Type.list, [Value(Type.int, 1), Value(Type.int, 2)]),
            Value(Type.list, [Value(Type.int, 1), Value(Type.int, 2)])
        )

    def test_Assert_with_error(self):
        test = Test(ConfigurationParameter(), MethodHandler())
        with self.assertRaises(AssertionError):
            test.Assert(Value(Type.string, "1"), Value(Type.string, "2"))

        with self.assertRaises(AssertionError):
            test.Assert(Value(Type.int, 2), Value(Type.int, 1))

        with self.assertRaises(AssertionError):
            test.Assert(Value(Type.float, 1.1), Value(Type.float, 1.2))

        with self.assertRaises(AssertionError):
            test.Assert(
                Value(Type.list, [Value(Type.int, 1), Value(Type.int, 2)]),
                Value(Type.list, [Value(Type.int, 2), Value(Type.int, 2)])
            )


if __name__ == '__main__':
    unittest.main()
