#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports
import pytest

from instal.parser.v2.parser import InstalPyParser
from instal.interfaces import ast as ASTs
from instal.compiler.query_compiler import InstalQueryCompiler

class TestQueryCompiler:

    def test_single_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))

        result = compiler.compile(data)

        assert(isinstance(result, str))
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% n/a",
                    "%-------------------------------",
                    "%%",
                    "",
                    "#program base.",
                    "",
                    "%% Query of test at 0",
                    "extObserved(test, 0).",
                    "_eventSet(0).",
                    "",
                    ]
        assert(len(result.split("\n")) ==  len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)

    def test_two_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))
        data.append(ASTs.QueryAST(ASTs.TermAST("second")))

        result = compiler.compile(data)

        assert(isinstance(result, str))
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% n/a",
                    "%-------------------------------",
                    "%%",
                    "",
                    "#program base.",
                    "",
                    "%% Query of test at 0",
                    "extObserved(test, 0).",
                    "_eventSet(0).",
                    "",
                    "%% Query of second at 1",
                    "extObserved(second, 1).",
                    "_eventSet(1).",
                    "",
                    ]
        assert(len(result.split("\n")) ==  len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)

    def test_explicit_time_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))
        data.append(ASTs.QueryAST(ASTs.TermAST("second"), time=3))

        result = compiler.compile(data)

        assert(isinstance(result, str))
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% n/a",
                    "%-------------------------------",
                    "%%",
                    "",
                    "#program base.",
                    "",
                    "%% Query of test at 0",
                    "extObserved(test, 0).",
                    "_eventSet(0).",
                    "",
                    "%% Query of second at 3",
                    "extObserved(second, 3).",
                    "_eventSet(3).",
                    ""
                    ]
        assert(len(result.split("\n")) ==  len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)

    def test_explicit_source_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test"),
                                       parse_source=["custom"]))

        result = compiler.compile(data)

        assert(isinstance(result, str))
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% custom",
                    "%-------------------------------",
                    "%%",
                    "",
                    "#program base.",
                    "",
                    "%% Query of test at 0",
                    "extObserved(test, 0).",
                    "_eventSet(0).",
                    ""
                    ]
        assert(len(result.split("\n")) ==  len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)
