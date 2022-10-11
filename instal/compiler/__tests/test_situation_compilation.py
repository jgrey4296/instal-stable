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
from unittest import mock
from instal.compiler.situation_compiler import InstalSituationCompiler
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestSituationCompiler(unittest.TestCase):
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

    def test_one_fact_situation(self):
        """ initially/iaf -> .lp """
        compiler = InstalSituationCompiler()
        data     = []
        data.append(ASTs.InitiallyAST([ASTs.TermAST("test")],
                                      inst=ASTs.TermAST("testInst")))

        result = compiler.compile(data)
        self.assertIsInstance(result, str)
        expected = [
            "#program base.",
            "",
            "% initially: test (if [conditions])",
            "holdsat(test, testInst, I) :- start(I),",
            "institution(testInst),",
            "inertialFluent(test, testInst),",
            "holdsat(live(testInst), testInst, I),",
            "true.",
            ""
            ]
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x.strip(),y)

    def test_two_fact_situation(self):
        """ initially/iaf -> .lp """
        compiler = InstalSituationCompiler()
        data     = []
        data.append(ASTs.InitiallyAST([ASTs.TermAST("first"),
                                       ASTs.TermAST("second")],
                                      inst=ASTs.TermAST("testInst")))

        result = compiler.compile(data)
        self.assertIsInstance(result, str)
        expected = [
            "#program base.",
            "",
            "% initially: first (if [conditions])",
            "holdsat(first, testInst, I) :- start(I),",
            "institution(testInst),",
            "inertialFluent(first, testInst),",
            "holdsat(live(testInst), testInst, I),",
            "true.",
            "",
            "% initially: second (if [conditions])",
            "holdsat(second, testInst, I) :- start(I),",
            "institution(testInst),",
            "inertialFluent(second, testInst),",
            "holdsat(live(testInst), testInst, I),",
            "true.",
            ]
        self.assertEqual(len(result.strip().split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x.strip(),y)



    def test_two_situations(self):
        """ initially/iaf -> .lp """
        compiler = InstalSituationCompiler()
        data     = []
        data.append(ASTs.InitiallyAST([ASTs.TermAST("blah")],
                                           inst=ASTs.TermAST("firstInst")))

        data.append(ASTs.InitiallyAST([ASTs.TermAST("bloo")],
                                           inst=ASTs.TermAST("secondInst")))

        result = compiler.compile(data)
        self.assertIsInstance(result, str)
        expected = [
            "#program base.",
            "",
            "% initially: blah (if [conditions])",
            "holdsat(blah, firstInst, I) :- start(I),",
            "institution(firstInst),",
            "inertialFluent(blah, firstInst),",
            "holdsat(live(firstInst), firstInst, I),",
            "true.",
            "",
            "% initially: bloo (if [conditions])",
            "holdsat(bloo, secondInst, I) :- start(I),",
            "institution(secondInst),",
            "inertialFluent(bloo, secondInst),",
            "holdsat(live(secondInst), secondInst, I),",
            "true.",
            "",
            ]
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x.strip(),y)


    @unittest.skip("todo")
    def test_fact_situation_with_conditions(self):
        pass
if __name__ == '__main__':
    unittest.main()
