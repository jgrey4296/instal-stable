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
from unittest import mock

from instal.parser.pyparse_institution import InstalPyParser
from instal.interfaces.ast import QueryTotalityAST
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

        cls.dsl = InstalPyParser()


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_simple_query(self):
        result = self.dsl.parse_query("observed person(bob) in greeting")
        self.assertIsInstance(result, QueryTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.body[0].head.value, "person")
        self.assertEqual(result.body[0].head.params[0].value, "bob")

    def test_simple_query_at_time(self):
        result = self.dsl.parse_query("observed person(bob) in greeting at 5")
        self.assertIsInstance(result, QueryTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.body[0].head.value, "person")
        self.assertEqual(result.body[0].head.params[0].value, "bob")
        self.assertEqual(result.body[0].time, 5)


    def test_multi_query(self):
        result = self.dsl.parse_query("observed person(bob) in greeting\nobserved person(jill) in greeting")
        self.assertIsInstance(result, QueryTotalityAST)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.body[0].head.value, "person")
        self.assertEqual(result.body[0].head.params[0].value, "bob")
        self.assertEqual(result.body[1].head.value, "person")
        self.assertEqual(result.body[1].head.params[0].value, "jill")


    def test_multi_query_with_time(self):
        result = self.dsl.parse_query("observed person(bob) in greeting at 5\nobserved person(jill) in greeting at 10")
        self.assertIsInstance(result, QueryTotalityAST)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.body[0].head.value, "person")
        self.assertEqual(result.body[0].head.params[0].value, "bob")
        self.assertEqual(result.body[0].time, 5)
        self.assertEqual(result.body[1].head.value, "person")
        self.assertEqual(result.body[1].head.params[0].value, "jill")
        self.assertEqual(result.body[1].time, 10)

if __name__ == '__main__':
    unittest.main()
