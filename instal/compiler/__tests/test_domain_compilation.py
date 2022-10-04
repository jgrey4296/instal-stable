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
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.interfaces import ast as ASTs
from unittest import mock
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestDomainCompiler(unittest.TestCase):
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

    def test_one_type_domain(self):
        """ initially/iaf -> .lp """
        compiler = InstalDomainCompiler()
        data     = []
        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Person"),
                                            [ASTs.TermAST("bill"),
                                             ASTs.TermAST("jill")]))

        result = compiler.compile(data)
        self.assertIsInstance(result, str)
        expected = [
            "%%",
            "%-------------------------------",
            "% Domain Specification",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "#program base.",
            "",
            "person(bill).",
            "person(jill).",
            ]
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)

    def test_two_type_domain(self):
        """ initially/iaf -> .lp """
        compiler = InstalDomainCompiler()
        data     = []
        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Person"),
                                            [ASTs.TermAST("bill"),
                                             ASTs.TermAST("jill")]))

        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Book"),
                                            [ASTs.TermAST("book1"),
                                             ASTs.TermAST("book2")]))

        result = compiler.compile(data)
        self.assertIsInstance(result, str)
        expected = [
            "%%",
            "%-------------------------------",
            "% Domain Specification",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "#program base.",
            "",
            "person(bill).",
            "person(jill).",
            "book(book1).",
            "book(book2).",
            ]
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)




if __name__ == '__main__':
    unittest.main()
