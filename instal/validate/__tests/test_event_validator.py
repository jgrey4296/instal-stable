#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.validate.event_validator import EventValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM
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

class TestEventValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ EventValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_basic_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "event_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_basic_inst_fail(self):
        """
        a report is generated if an institutional event is not generated
        """
        file_name = data_path / "event_check_inst_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertTrue(result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        self.assertEqual(result[logmod.WARNING][0].msg, "Institutional Event is not generated")

    def test_basic_chain_pass(self):
        """
        reports aren't generated when institutional events generate
        further institutional events
        """
        file_name = data_path / "event_check_chain_pass.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_basic_ex_fail(self):
        """
        a report is generated if an external event is not used
        """
        file_name = data_path / "event_check_ex_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertTrue(result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        self.assertEqual(result[logmod.WARNING][0].msg, "Unused External Event")



    def test_basic_fail_detail(self):
        """
        Check appropriate details of a report
        """
        file_name = data_path / "event_check_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 2)
        msgs = [x.msg for x in result[logmod.WARNING]]
        self.assertIn("Unused External Event", msgs)
        self.assertIn("Institutional Event is not generated", msgs)



if __name__ == '__main__':
    unittest.main()
