#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from instal.parser.v2.parser import InstalPyParser
from instal.interfaces import ast as ASTs
from instal.compiler.query_compiler import InstalQueryCompiler
from unittest import mock
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestQueryCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_single_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))

        result = compiler.compile(data)

        self.assertIsInstance(result, str)
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% ",
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
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)

    def test_two_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))
        data.append(ASTs.QueryAST(ASTs.TermAST("second")))

        result = compiler.compile(data)

        self.assertIsInstance(result, str)
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% ",
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
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)

    def test_explicit_time_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test")))
        data.append(ASTs.QueryAST(ASTs.TermAST("second"), time=3))

        result = compiler.compile(data)

        self.assertIsInstance(result, str)
        expected = ["%%",
                    "%-------------------------------",
                    "% Query Specification",
                    "% ",
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
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)

    def test_explicit_source_query(self):
        """ query/iaq -> lp """
        compiler = InstalQueryCompiler()
        data = []
        data.append(ASTs.QueryAST(ASTs.TermAST("test"),
                                       parse_source=["custom"]))

        result = compiler.compile(data)

        self.assertIsInstance(result, str)
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
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)



if __name__ == '__main__':
    unittest.main()
