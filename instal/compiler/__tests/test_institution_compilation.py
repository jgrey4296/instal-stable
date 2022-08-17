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
from instal.parser.pyparse_institution import InstalPyParser
from instal.compiler.institution_compiler import InstalInstitutionCompiler, CompileUtil
from instal.interfaces import ast as ASTs
from unittest import mock
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionCompiler(unittest.TestCase):
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
        cls.compiler = InstalInstitutionCompiler()


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





    def test_situation_compilation(self):
        """ initially/iaf -> .lp """
        pass

    def test_query_compilation(self):
        """ query/iaq -> lp """
        pass

    def test_domain_compilation(self):
        """ domainspec/idc -> lp """
        pass



if __name__ == '__main__':
    unittest.main()
