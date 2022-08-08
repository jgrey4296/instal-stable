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
import instal.interfaces.ast as ASTs
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestSituationParser(unittest.TestCase):
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

    def test_simple_situation(self):
        result = self.dsl.parse_situation("initially basicfact in greeting")
        self.assertIsInstance(result, ASTs.FactTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result.body[0].body), 1)
        self.assertFalse(result.body[0].conditions)
        self.assertEqual(result.body[0].inst.value, "greeting")

    def test_simple_situation_with_param(self):
        result = self.dsl.parse_situation("initially basic(blah) in greeting")
        self.assertIsInstance(result, ASTs.FactTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result.body[0].body), 1)
        self.assertEqual(result.body[0].inst.value, "greeting")
        self.assertTrue(result.body[0].body[0].value, "basic")
        self.assertTrue(result.body[0].body[0].params[0].value, "blah")

    def test_multi_initially(self):
        result = self.dsl.parse_situation("initially basic(blah) in greeting\ninitially other in greeting")


if __name__ == '__main__':
    unittest.main()
