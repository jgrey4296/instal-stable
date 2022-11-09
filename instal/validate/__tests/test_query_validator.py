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

from instal.validate.query_validator import QueryValidator
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

# TODO implement and test query validator
class TestQueryValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ QueryValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_trivial_pass(self):
        """
        Validator no reports are generated on proper use of events
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ QueryValidator() ])
        data      = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_basic_pass(self):
        """
        Validator no reports are generated on proper use of events
        """
        inst_file_name  = data_path / "basic_query_inst.ial"
        query_file_name = data_path / "basic_query_pass.iaq"
        runner          = validate.InstalValidatorRunner([ QueryValidator() ])
        inst_data       = parser.parse_institution(inst_file_name)
        query_data      = parser.parse_query(query_file_name)
        self.assertIsInstance(inst_data[0], iAST.InstitutionDefAST)
        self.assertIsInstance(query_data[0], iAST.QueryAST)

        result = runner.validate(inst_data + query_data)
        self.assertFalse(result)


    def test_basic_fail(self):
        """
        Validator no reports are generated on proper use of events
        """
        inst_file_name  = data_path / "basic_query_inst.ial"
        query_file_name = data_path / "basic_query_fail.iaq"
        runner    = validate.InstalValidatorRunner([ QueryValidator() ])
        inst_data  = parser.parse_institution(inst_file_name)
        query_data = parser.parse_query(query_file_name)
        self.assertIsInstance(inst_data[0], iAST.InstitutionDefAST)
        self.assertIsInstance(query_data[0], iAST.QueryAST)

        result = runner.validate(inst_data + query_data)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
