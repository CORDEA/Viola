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

import re

import ply.lex as lex

from src.impl.enum.type import Type
from src.impl.model.value import Value

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2015-12-20"

tokens = (
    "VAR", "METHOD", "IN", "ANNOT",
    "IF", "ELIF",
    "STRING", "NUMBER",
    "NONE", "TRUE", "FALSE",
    "PLUS", "MINUS", "TIMES", "DIVIDE", "MODULUS", "POWER", "SQRT",
    "ARRAY", "BRACKET_RIGHT", "BRACKET_LEFT",
    "EEQUALS", "ENEQUALS", "EQUALS",
    "INDENT",
    "NL"
)

LOWER = r'[a-z]'
UPPER = r'[A-Z]'
STRINGS = r'[a-zA-Z]'
t_METHOD = r'(' + UPPER + STRINGS + r'+\')?' + UPPER + STRINGS + r'+'
t_IN = r'<'
t_IF = r'>'
t_ELIF = r'\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\*\*'
t_SQRT = r'//'
t_MODULUS = r'%'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_EEQUALS = r'=='
t_ENEQUALS = r'!='
t_ARRAY = r'\.\.'
t_BRACKET_LEFT = r'\('
t_BRACKET_RIGHT = r'\)'


def t_VAR(t):
    r'[a-z]+\w*'
    if t.value == "discard":
        t.value = Value(Type.discard, t.value)
    else:
        t.value = Value(Type.var, t.value)
    return t


def t_ANNOT(t):
    r'\[\w+\]'
    r = re.compile(r'\[(\w+)\]').match(t.value)
    if r:
        t.value = Value(Type.string, r.group(1))
    return t


def t_STRING(t):
    r'"([^\n"]*)"'
    r = re.compile(r'"([^\n"]*)"').match(t.value)
    if r:
        t.value = Value(Type.string, str(r.group(1)))
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if len(re.findall(r'\d+(\.\d+)?', t.value)[0]) > 0:
        t.value = Value(Type.float, float(t.value))
    else:
        t.value = Value(Type.int, int(t.value))
    return t


def t_TRUE(t):
    r'(?<=[^\w\n])T(?!\w)'
    t.value = Value(Type.bool, True)
    return t


def t_FALSE(t):
    r'(?<=[^\w\n])F(?!\w)'
    t.value = Value(Type.bool, False)
    return t


def t_INDENT(t):
    r'\ {4,}|\t+'
    if re.compile(r'(?: {4})+').match(t.value):
        s = len(t.value.split('    ')) - 1
        t.value = s
    elif re.compile(r'\t+').match(t.value):
        s = len(t.value.split('\t')) - 1
        t.value = s
    else:
        raise IndentationError()
    return t


def t_COMMENT(t):
    r'[\ \t]*\#[^\n]*'
    pass


def t_NL(t):
    r'\n'
    t.lexer.lineno += 1
    return t


t_ignore = ""


def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()
if __name__ == '__main__':
    lex.runmain(lexer)
