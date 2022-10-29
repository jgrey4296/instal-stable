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

from instal.checkers.fluent_check import FluentCheck
from instal.interfaces import ast as iAST
from instal.interfaces import checker
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
data_path = files("instal.checkers.__tests.__data")
##-- end data


class TestCheck(unittest.TestCase):
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
        runner = checker.InstalCheckRunner([ FluentCheck() ])
        self.assertIsInstance(runner, checker.InstalCheckRunner)
        self.assertIsNotNone(runner.checkers)

    def test_basic_pass(self):
        """
        Check there are no reports if a consistent institution is defined
        """
        file_name = "fluent_check_pass.ial"
        runner    = checker.InstalCheckRunner([ FluentCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertFalse(result)

    def test_basic_initiate_fail(self):
        """
        Check a report is generated if an inertial fluent isn't initiated anywhere.
        """
        file_name = "fluent_check_initiate_fail.ial"
        runner    = checker.InstalCheckRunner([ FluentCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        self.assertEqual(result[logmod.WARNING][0].msg, "Non-Initiated Inertial Fluent")

    def test_basic_terminate_fail(self):
        """
        Check a report is generated if an inertial fluent isn't terminated anywhere
        """
        file_name = "fluent_check_terminate_fail.ial"
        runner    = checker.InstalCheckRunner([ FluentCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        self.assertEqual(result[logmod.WARNING][0].msg, "Non-Terminated Inertial Fluent")

    def test_basic_transient_fail(self):
        """
        Check a report is generated if a transient fluent isn't used as the head of a `when` rule.
        """
        file_name = "fluent_check_transient_fail.ial"
        runner    = checker.InstalCheckRunner([ FluentCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 1)
        self.assertEqual(result[logmod.WARNING][0].msg, "Unmentioned Transient Fluent")






if __name__ == '__main__':
    unittest.main()
