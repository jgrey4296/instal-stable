#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.compiler.util import CompileUtil
from instal.interfaces import ast as ASTs
from instal.parser.pyparse_institution import InstalPyParser

##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestCompilerUtils(unittest.TestCase):
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

    def test_basic_term(self):
        term   = ASTs.TermAST("test")
        result = CompileUtil.compile_term(term)
        self.assertEqual(result, "test")

    def test_term_with_params(self):
        term = ASTs.TermAST("test", params=[ASTs.TermAST("first"),
                                            ASTs.TermAST("second")])
        result = CompileUtil.compile_term(term)
        self.assertEqual(result, "test(first, second)")


if __name__ == '__main__':
    unittest.main()
