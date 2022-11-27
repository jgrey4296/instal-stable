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

from instal.validate.deontic_validator import DeonticValidator
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


class TestDeonticValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ DeonticValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_empty_pass(self):
        """
        check no reports are generated on an empty institution
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_basic_fail(self):
        """
        check reports are generated on improper use of deontics
        """
        file_name = data_path / "deontic_check_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])

        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertTrue(the_exc.args[1])
        self.assertEqual(len(the_exc.args[1][40]), 2)

        bad_asts = {x.ast.params[0].signature for x in the_exc.args[1][40]}
        self.assertEqual(bad_asts, set(["aFluent/0", "testEvent/0"]))


    def test_basic_pass(self):
        """
        check no reports are generated on deontics applied to institutional events
        """
        file_name = data_path / "deontic_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)

    def test_obligation_fluent_name_duplication_fail(self):
        """

        """
        file_name = data_path / "obl_deontic_name_duplication_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)
        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertTrue(the_exc.args)
        self.assertEqual(len(the_exc.args[1][40]), 2)
        msgs = [x.msg for x in the_exc.args[1][40]]
        self.assertIn("Duplicate obligation declared", msgs)
        self.assertIn("Obligation Use does not match Declaration", msgs)


    def test_obligation_fluent_structure_fail(self):
        """

        """
        file_name = data_path / "obl_deontic_check_structure_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)
        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertTrue(the_exc.args)
        self.assertEqual(len(the_exc.args[1][40]), 1)
        msg = the_exc.args[1][40][0].msg
        self.assertEqual(msg, "Obligation Use does not match Declaration")


    def test_obligation_fluent_def_fail(self):
        """
        Report on obligations not using institutional events as parameters
        """
        file_name = data_path / "obl_deontic_check_def_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)
        with self.assertRaises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        self.assertTrue(the_exc.args)
        self.assertEqual(len(the_exc.args[1][40]), 1)
        msg = the_exc.args[1][40][0].msg
        self.assertEqual(msg, "Obligation Declared with an incompatiable argument")


    def test_obligation_fluent_pass(self):
        """

        """
        file_name = data_path / "obl_deontic_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.validate(data)
        self.assertFalse(result)




##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
