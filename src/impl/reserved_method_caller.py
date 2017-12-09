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

import inspect

from src.impl.model.reserved_method import ReservedMethod
from src.impl.reserved.file import File
from src.impl.reserved.list import List
from src.impl.reserved.out import Out
from src.impl.reserved.system import System
from src.impl.reserved.test import Test

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-21"


class ReservedMethodCaller:
    def __init__(self, cp, handler):
        self.cp = cp
        self.handler = handler

    @classmethod
    def __methods(cls):
        reserved = {}
        list_methods = inspect.getmembers(List, predicate=inspect.ismethod)
        for method in list_methods:
            if "__init__" != method:
                reserved[List.__name__ + "'" + method[0]] = [List, method[1]]
        out_methods = inspect.getmembers(Out, predicate=inspect.ismethod)
        for method in out_methods:
            if "__init__" != method:
                reserved[method[0]] = [Out, method[1]]
        file_methods = inspect.getmembers(File, predicate=inspect.ismethod)
        for method in file_methods:
            if "__init__" != method:
                reserved[File.__name__ + "'" + method[0]] = [File, method[1]]
        test_methods = inspect.getmembers(Test, predicate=inspect.ismethod)
        for method in test_methods:
            if "__init__" != method:
                reserved[Test.__name__ + "'" + method[0]] = [Test, method[1]]
        system_methods = inspect.getmembers(System, predicate=inspect.ismethod)
        for method in system_methods:
            if "__init__" != method:
                reserved[System.__name__ + "'" + method[0]] = [System, method[1]]
        return reserved

    @classmethod
    def is_reserved_method(cls, name):
        return name in cls.__methods()

    def core(self, name, args):
        reserved = self.__methods()

        if name in reserved:
            lst = reserved[name]
            args_len = len(args)
            arg_spec = inspect.getargspec(lst[1])
            class_method_args = len(arg_spec.args) - 1
            defaults = len(arg_spec.defaults) if arg_spec.defaults is not None else 0
            if class_method_args - defaults <= args_len <= class_method_args:
                return ReservedMethod(lst[0], lst[1], args)
        print "error"

    def fire(self, rm):
        self = self
        cls = rm.cls
        method = rm.method
        args = rm.args
        args_len = len(args)
        ins = cls(self.cp, self.handler)
        if args_len == 0:
            return method(ins)
        elif args_len == 1:
            return method(ins, args[0])
        elif args_len == 2:
            return method(ins, args[0], args[1])
