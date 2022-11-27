#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
from importlib.resources import files
from instal.parser.v2.parser import InstalPyParser

import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.utils import TERM
from instal.validate.declaration_type_validator import DeclarationTypeValidator
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


# TODO implement and test declaration types
class TestDeclarationTypeValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_empty_pass(self):
        """
        no reports are generated on an empty inst
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_basic_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "term_type_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    @unittest.expectedFailure
    def test_basic_fail(self):
        """
        reports are generated on type conflicts
        """
        file_name = data_path / "term_type_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertTrue(result)



##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
