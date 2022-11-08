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

from instal.validate.institution_structure_validator import \
    InstitutionStructureValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.utils import TERM

##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root


class TestInstitutionStructureValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ InstitutionStructureValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_basic_validator_run(self):
        " Run a simple validate on an empty institution. "
        runner = validate.InstalValidatorRunner([ InstitutionStructureValidator() ])

        basic_inst = iAST.InstitutionDefAST(TERM.parse_string("test_inst")[0])

        results = runner.validate([basic_inst])
        # Provides warnings about the fluents,events,types,rules and facts being empty:
        self.assertIn(logmod.WARNING, results)
        self.assertTrue(results[logmod.WARNING])
        self.assertEqual(len(results[logmod.WARNING]), 5)

if __name__ == '__main__':
    unittest.main()
