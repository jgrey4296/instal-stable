#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.interfaces import checker
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
class SimpleChecker(checker.InstalChecker_i):
    def check(self, data):
        match data[0]:
            case None:
                raise Exception("SimpleChecker got None")
            case True:
                self.info("A Simple Report")
            case "warning":
                self.warning("A Simple Warning")

class SecondChecker(checker.InstalChecker_i):
    def check(self, data):
        self.info("Second Check Report")



class ExtractCheck(checker.InstalChecker_i):

    def extract(self, asts):
        return asts[0].body

    def check(self, data):
        strings = [str(x) for x in data]
        if "test" not in strings:
            self.error("No test fact found", data)
        if "blah(bloo,bloo)" not in strings:
            raise Exception("No blah fact found", data)

##-- end util classes

class TestCheckRunner(unittest.TestCase):
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
        runner = checker.InstalCheckRunner()
        self.assertIsInstance(runner, checker.InstalCheckRunner)

    def test_initial_with_checker(self):
        runner = checker.InstalCheckRunner([ SimpleChecker() ])
        self.assertIsInstance(runner, checker.InstalCheckRunner)
        self.assertIsNotNone(runner.checkers)

    def test_initial_failure(self):
        """
        Verify a checker throwing an error is recorded as level 101
        """
        runner = checker.InstalCheckRunner([ SimpleChecker() ])
        with self.assertRaises(Exception) as cm:
            runner.check(None)

        self.assertEqual(cm.exception.args[1][101][0].args[0], "SimpleChecker got None")

    def test_simple_info_report(self):
        """
        Verify a checker reporting at INFO level is recorded
        """
        runner = checker.InstalCheckRunner([ SimpleChecker() ])
        results = runner.check(True)
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 1)
        self.assertEqual(results[logmod.INFO][0].msg, "A Simple Report")

    def test_simple_warning_report(self):
        """
        Verify a checker reporting at WARNING level is recorded
        """
        runner = checker.InstalCheckRunner([ SimpleChecker() ])
        results = runner.check("warning")
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.WARNING, results)
        self.assertEqual(len(results[logmod.WARNING]), 1)
        self.assertEqual(results[logmod.WARNING][0].msg, "A Simple Warning")


    def test_multi_checkers(self):
        """
        Verify multiple checkers can run without interference
        """
        runner = checker.InstalCheckRunner([ SimpleChecker(), SecondChecker() ])
        results = runner.check(True)
        self.assertIsInstance(results, dict)
        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 2)
        msgs = [x.msg for x in results[logmod.INFO]]
        self.assertIn("A Simple Report", msgs)
        self.assertIn("Second Check Report", msgs)

    def test_multi_checkers_all_run(self):
        """
        Verify multiple checkers can report at different levels
        """
        runner = checker.InstalCheckRunner([ SimpleChecker(), SecondChecker() ])
        results = runner.check("warning")
        self.assertIsInstance(results, dict)

        self.assertIn(logmod.INFO, results)
        self.assertEqual(len(results[logmod.INFO]), 1)
        msgs = [x.msg for x in results[logmod.INFO]]
        self.assertIn("Second Check Report", msgs)

        self.assertIn(logmod.WARN, results)
        self.assertEqual(len(results[logmod.WARN]), 1)
        self.assertEqual(results[logmod.WARN][0].msg, "A Simple Warning")


    def test_simple_extractor(self):
        """
        Verify extractors can process input to provide lower level details
        """
        simple_ast = iAST.InitiallyAST([TERM.parse_string("test")[0],
                                        TERM.parse_string("blah(bloo,bloo)")[0]])

        runner = checker.InstalCheckRunner([ ExtractCheck() ])
        results = runner.check([simple_ast])
        self.assertFalse(results)



if __name__ == '__main__':
    unittest.main()
