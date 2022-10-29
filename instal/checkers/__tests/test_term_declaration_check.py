#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
from importlib.resources import files
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.interfaces import ast as iAST
from instal.interfaces import checker
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM
from instal.checkers.term_declaration_check import TermDeclarationCheck
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root

##-- data
data_path = files("instal.checkers.__tests.__data")
##-- end data


class TestTermDeclarationCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging.setLevel(logmod.NOTSET)
        logging.addHandler(cls.file_h)


    @classmethod
    def tearDownClass(cls):
        logging.removeHandler(cls.file_h)

    def test_initial_ctor_with_checker(self):
        runner = checker.InstalCheckRunner([ TermDeclarationCheck() ])
        self.assertIsInstance(runner, checker.InstalCheckRunner)
        self.assertIsNotNone(runner.checkers)

    def test_basic_pass(self):
        """
        Check no reports are generated on proper use of events
        """
        file_name = "term_decl_pass.ial"
        runner    = checker.InstalCheckRunner([ TermDeclarationCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertFalse(result)

    def test_basic_fail(self):
        """
        Check a report is generated for declarations that aren't used
        """
        file_name = "term_decl_fail.ial"
        runner    = checker.InstalCheckRunner([ TermDeclarationCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)

        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        msgs = {x.msg for x in result[logmod.WARNING]}
        self.assertEqual(len(msgs), 1)
        self.assertIn("Term declared without use", msgs)
        self.assertEqual(repr(result[logmod.WARNING][0].ast.head), "exEv(Test,Test2)")

    def test_basic_use_fail(self):
        """
        Check an error report is generated for term use without declaration
        """
        file_name = "term_decl_use_fail.ial"
        runner    = checker.InstalCheckRunner([ TermDeclarationCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            result = runner.check(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        self.assertEqual(len(result[logmod.ERROR]), 1)
        self.assertEqual(result[logmod.ERROR][0].msg, "Term used without declaration")
        self.assertEqual(str(result[logmod.ERROR][0].ast), "badEv")

    def test_basic_signature_fail(self):
        """
        Check an error report is generated for signature mismatches
        """
        file_name = "term_decl_signature_fail.ial"
        runner    = checker.InstalCheckRunner([ TermDeclarationCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            result = runner.check(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        self.assertEqual(len(result[logmod.ERROR]), 1)
        self.assertEqual(result[logmod.ERROR][0].msg, "Term used without declaration")
        self.assertEqual(str(result[logmod.ERROR][0].ast), "simpleEv(Test)")



if __name__ == '__main__':
    unittest.main()
