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

from instal.checkers.name_duplication_check import NameDuplicationCheck
from instal.parser.v2.parser import InstalPyParser
from instal.interfaces import ast as iAST
from instal.interfaces import checker
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
# data_file = data_path.joinpath("filename.ext")
# data_text = data_file.read_text()
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
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])
        self.assertIsInstance(runner, checker.InstalCheckRunner)
        self.assertIsNotNone(runner.checkers)

    def test_fluent_duplicate(self):
        """
        Check an error report is raised when a fluent is duplicated
        """
        test_file = "name_duplication_test1.ial"
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_event_duplicate(self):
        """
        Check an event duplication report is generated
        """
        test_file = "name_duplication_test1.ial"
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Event Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_event_conflict(self):
        """
        Check an event-fluent conflict is recognized
        """
        test_file = "name_duplication_test1.ial"
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Event-Fluent Name Conflict",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_type_duplicate(self):
        """
        Check a typedec duplication report is raised
        """
        test_file = "name_duplication_test1.ial"
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate TypeDec Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_type_fluent_conflict(self):
        """
        Check a typedec-fluent conflict report is raised
        """
        test_file = "name_duplication_test1.ial"
        runner    = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("TypeDec-Fluent Name Conflict",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_type_event_conflict(self):
        """
        check typedec-event conflicts are recognized
        """
        test_file = "name_duplication_test1.ial"
        runner    = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("TypeDec-Event Name Conflict",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_fluent_duplication_with_params(self):
        """
        Check exact fluent parameters can cause duplication reports
        """
        test_file = "name_params_duplication_test.ial"
        runner    = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertEqual(len(the_exc.args[1][logmod.ERROR]), 1)
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_duplication_with_vars(self):
        """
        Check fluents with the same variables trigger duplication reports
        """
        test_file = "name_vars_duplication_test.ial"
        runner    = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath(test_file).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_fluent_duplication_with_numbered_vars(self):
        """
        TODO
        Check fluent declaration with vars only differing by index number
        generate duplication reports
        """
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath("name_vars_numbered_duplication_test.ial").read_text()
        data = InstalPyParser().parse_institution(text, parse_source="name_params_duplication_test.ial")
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


if __name__ == '__main__':
    unittest.main()
