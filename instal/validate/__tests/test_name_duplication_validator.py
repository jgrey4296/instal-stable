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

from instal.validate.name_duplication_validator import NameDuplicationValidator
from instal.parser.v2.parser import InstalPyParser
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

##-- data
data_path = files("instal.validate.__tests.__data")
# data_file = data_path.joinpath("filename.ext")
# data_text = data_file.read_text()
##-- end data
parser = InstalPyParser()


class TestNameDuplicationValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_fluent_duplicate(self):
        """
        check an error report is raised when a fluent is duplicated
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_event_duplicate(self):
        """
        check an event duplication report is generated
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Event Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_event_conflict(self):
        """
        check an event-fluent conflict is recognized
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        self.assertTrue(conflicts)

    def test_type_duplicate(self):
        """
        check a typedec duplication report is raised
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate TypeDec Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_type_fluent_conflict(self):
        """
        check a typedec-fluent conflict report is raised
        """
        test_file = data_path / "type_fluent_conflict_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        self.assertTrue(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        self.assertIn(iAST.FluentAST, asts)
        self.assertIn(iAST.DomainSpecAST, asts)



    def test_type_ex_event_conflict(self):
        """
        check typedec-event conflicts are recognized
        """
        test_file = data_path / "type_ex_event_conflict.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        self.assertTrue(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        self.assertIn(iAST.EventAST, asts)
        self.assertIn(iAST.DomainSpecAST, asts)

    def test_type_inst_event_conflict(self):
        """
        check typedec-event conflicts are recognized
        """
        test_file = data_path / "type_inst_event_conflict.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        self.assertTrue(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        self.assertIn(iAST.EventAST, asts)
        self.assertIn(iAST.DomainSpecAST, asts)



    def test_fluent_duplication_with_params(self):
        """
        check exact fluent parameters can cause duplication reports
        """
        test_file = data_path / "name_params_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertEqual(len(the_exc.args[1][logmod.ERROR]), 1)
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_duplication_with_vars(self):
        """
        check fluents with the same variables trigger duplication reports
        """
        test_file = data_path / "name_vars_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_fluent_duplication_with_numbered_vars(self):
        """
        check fluent declaration with vars only differing by index number
        generate duplication reports
        """
        runner = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        file_name = data_path / "name_vars_numbered_duplication_test.ial"
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertIn("Duplicate Fluent Declaration",
                      {x.msg for x in the_exc.args[1][logmod.ERROR]})


##-- ifmain
if __name__ == '__main__':
    unittest.main()

##-- end ifmain
