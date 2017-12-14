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
from src.impl.reserved.list import List
from src.impl.reserved.out import Out
from src.impl.reserved.test import Test

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2017-12-13"


class TestMethodHandler(unittest.TestCase):

    def test_expression_from_tuple(self):
        handler = MethodHandler()
        actual = handler.expression_from_tuple(
            Value(Type.int, 1),
            {}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(1, actual.value)

        actual = handler.expression_from_tuple(
            Value(Type.var, "a"),
            {"a": Value(Type.int, 1)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(1, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "+", Value(Type.int, 1)),
            {"a": Value(Type.int, 1)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(2, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "-", Value(Type.int, 1)),
            {"a": Value(Type.int, 1)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(0, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "*", Value(Type.int, 3)),
            {"a": Value(Type.int, 2)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(6, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "/", Value(Type.int, 2)),
            {"a": Value(Type.int, 4)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(2, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "+", Value(Type.int, 1)),
            {"a": Value(Type.float, 1.1)}
        )
        self.assertEqual(Type.float, actual.value_type)
        self.assertEqual(2.1, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "-", Value(Type.float, 2.2)),
            {"a": Value(Type.float, 4.4)}
        )
        self.assertEqual(Type.float, actual.value_type)
        self.assertEqual(2.2, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "*", Value(Type.float, 2.5)),
            {"a": Value(Type.float, 4.1)}
        )
        self.assertEqual(Type.float, actual.value_type)
        self.assertEqual(10.25, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "+", Value(Type.int, -2)),
            {"a": Value(Type.int, -4)}
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(-6, actual.value)

        actual = handler.expression_from_tuple(
            (Value(Type.var, "a"), "-", Value(Type.float, -2.3)),
            {"a": Value(Type.float, -4.5)}
        )
        self.assertEqual(Type.float, actual.value_type)
        self.assertEqual(-2.2, actual.value)

        actual = handler.expression_from_tuple(
            (
                Value(Type.var, "a"),
                "+",
                Value(Type.int, 4),
                "*",
                Value(Type.int, 4),
                "-",
                Value(Type.var, "b"),
                "/",
                Value(Type.int, 4)
            ),
            {
                "a": Value(Type.int, 4),
                "b": Value(Type.int, 4),
            }
        )
        self.assertEqual(Type.int, actual.value_type)
        self.assertEqual(19, actual.value)

    def test_get_reserved_obj(self):
        handler = MethodHandler()
        actual = handler.get_reserved_obj(
            ["List'Init"],
            ConfigurationParameter()
        )
        self.assertEqual(type(List), type(actual.cls))
        self.assertEqual(0, len(actual.args))
        self.assertEqual("Init", actual.method.__name__)

        actual = handler.get_reserved_obj(
            [Value(Type.bool, True), "Eco"],
            ConfigurationParameter()
        )
        self.assertEqual(type(Out), type(actual.cls))
        self.assertEqual(1, len(actual.args))
        self.assertEqual(Type.bool, actual.args[0].value_type)
        self.assertEqual(True, actual.args[0].value)
        self.assertEqual("Eco", actual.method.__name__)

        actual = handler.get_reserved_obj(
            [Value(Type.string, "a"), "Test'Assert", Value(Type.string, "b")],
            ConfigurationParameter()
        )
        self.assertEqual(type(Test), type(actual.cls))
        self.assertEqual(2, len(actual.args))
        self.assertEqual(Type.string, actual.args[0].value_type)
        self.assertEqual("a", actual.args[0].value)
        self.assertEqual(Type.string, actual.args[1].value_type)
        self.assertEqual("b", actual.args[1].value)
        self.assertEqual("Assert", actual.method.__name__)


if __name__ == "__main__":
    unittest.main()
