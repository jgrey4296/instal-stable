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

from instal.parser.pyparse_institution import TERM
import instal.interfaces.ast as ASTs
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestTermParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

        cls.dsl = TERM


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_simple_term(self):
        result = self.dsl.parse_string("basic")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "basic")
        self.assertFalse(result.params)
        self.assertFalse(result.is_var)


    def test_term_with_param(self):
        result = self.dsl.parse_string("basic(aParam)")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "basic")
        self.assertTrue(result.params)
        self.assertEqual(result.params[0].value, "aParam")
        self.assertFalse(result.is_var)

    def test_term_with_multi_param(self):
        result = self.dsl.parse_string("basic(aParam, another)")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "basic")
        self.assertTrue(result.params)
        self.assertFalse(result.is_var)
        self.assertEqual(len(result.params), 2)
        self.assertEqual(result.params[0].value, "aParam")
        self.assertEqual(result.params[1].value, "another")

    def test_var_term(self):
        result = self.dsl.parse_string("Basic")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "Basic")
        self.assertFalse(result.params)
        self.assertTrue(result.is_var)

    def test_var_term_as_param(self):
        result = self.dsl.parse_string("basic(Param)")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "basic")
        self.assertTrue(result.params)
        self.assertTrue(result.params[0].is_var)

    def test_nested_term(self):
        result = self.dsl.parse_string("basic(other, another(nested, even(further)))")[0]
        self.assertIsInstance(result, ASTs.TermAST)
        self.assertEqual(result.value, "basic")
        self.assertEqual(len(result.params), 2)
        self.assertEqual(len(result.params[1].params), 2)
        self.assertEqual(result.params[1].params[1].value, "even")
        self.assertEqual(result.params[1].params[1].params[0].value, "further")


if __name__ == '__main__':
    unittest.main()
