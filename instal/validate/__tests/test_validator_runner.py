#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
from dataclasses import dataclass, field, InitVar
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.interfaces import validate
from instal.interfaces import ast as iAST
from instal.parser.v2.utils import TERM
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root

##-- util classes
@dataclass
class SimpleValidator(validate.InstalValidator_i):

    nodes : list = field(init=False, default_factory=list)

    def action_TermAST(self, visitor, node):
        self.nodes.append(node)

    def validate(self):
        match self.nodes[0].value:
            case "hardFail":
                raise Exception("told to hardFail")
            case "info report":
                self.info("A Simple Report")
            case "warning":
                self.warning("A Simple Warning")
            case _:
                self.info(self.nodes[0].value)



@dataclass
class SecondValidator(validate.InstalValidator_i):

    def action_TermAST(self, visitor, node):
        self.info("second validator fired")

##-- end util classes

class TestValidatorRunner(unittest.TestCase):
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

    def test_initial(self):
        runner = validate.InstalValidatorRunner()
        self.assertIsInstance(runner, validate.InstalValidatorRunner)

    def test_initial_with_validator(self):
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_initial_failure(self):
        """
        Verify a validate throwing an error is recorded as level 101
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        with self.assertRaises(Exception) as cm:
            runner.validate(iAST.TermAST("hardFail"))

        self.assertEqual(cm.exception.args[1][101][0].args[0], "told to hardFail")

    def test_simple_info_report(self):
        """
        Verify a validate reporting at INFO level is recorded
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        results = runner.validate(iAST.TermAST("info report"))
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 1)
        self.assertEqual(results[logmod.INFO][0].msg, "A Simple Report")

    def test_simple_warning_report(self):
        """
        Verify a validate reporting at WARNING level is recorded
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        results = runner.validate(iAST.TermAST("warning"))
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.WARNING, results)
        self.assertEqual(len(results[logmod.WARNING]), 1)
        self.assertEqual(results[logmod.WARNING][0].msg, "A Simple Warning")


    def test_multi_validators(self):
        """
        Verify multiple validators can run without interference
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator(), SecondValidator() ])
        results = runner.validate(iAST.TermAST("blah"))
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 2)
        msgs = [x.msg for x in results[logmod.INFO]]
        self.assertIn("blah", msgs)
        self.assertIn("second validator fired", msgs)

    def test_multi_validators_all_run(self):
        """
        Verify multiple validators can report at different levels
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator(), SecondValidator() ])
        results = runner.validate(iAST.TermAST("warning"))
        self.assertIsInstance(results, dict)

        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 1)
        msgs = [x.msg for x in results[logmod.INFO]]
        self.assertIn("second validator fired", msgs)

        self.assertIn(logmod.WARN, results)
        self.assertEqual(len(results[logmod.WARN]), 1)
        self.assertEqual(results[logmod.WARN][0].msg, "A Simple Warning")


if __name__ == '__main__':
    unittest.main()
