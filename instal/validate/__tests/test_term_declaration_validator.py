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
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM
from instal.validate.term_declaration_validator import TermDeclarationValidator
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
parser = InstalPyParser()


class TestTermDeclarationValidator(unittest.TestCase):
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

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)


    def test_basic_use_fail(self):
        """
        an error report is generated for term use without declaration
        """
        file_name = data_path / "term_decl_use_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            result = runner.validate(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        self.assertEqual(len(result[logmod.ERROR]), 1)
        self.assertEqual(result[logmod.ERROR][0].msg, "Term used without declaration")
        self.assertEqual(str(result[logmod.ERROR][0].ast), "badEv")


    def test_basic_signature_fail(self):
        """
        an error report is generated for signature mismatches
        """
        file_name = data_path / "term_decl_signature_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            result = runner.validate(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        self.assertEqual(len(result[logmod.ERROR]), 1)
        self.assertEqual(result[logmod.ERROR][0].msg, "Term used without declaration")
        self.assertEqual(str(result[logmod.ERROR][0].ast), "simpleEv(Test)")


    def test_type_declaration_usage_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "term_decl_pass.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    @unittest.expectedFailure
    def test_type_declaration_usage_fail(self):
        """
        a report is generated for declarations that aren't used
        """
        file_name = data_path / "term_decl_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)

        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        msgs = {x.msg for x in result[logmod.WARNING]}
        self.assertEqual(len(msgs), 1)
        self.assertIn("Term declared without use", msgs)
        self.assertEqual(repr(result[logmod.WARNING][0].ast.head), "exEv(Test,Test2)")




##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
