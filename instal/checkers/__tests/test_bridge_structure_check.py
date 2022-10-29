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

from instal.checkers.bridge_structure_check import BridgeStructureChecker
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
        runner = checker.InstalCheckRunner([ BridgeStructureChecker() ])
        self.assertIsInstance(runner, checker.InstalCheckRunner)
        self.assertIsNotNone(runner.checkers)

    def test_basic_pass(self):
        """
        Check a basic bridge + source + sink doesn't report
        """
        bridge_file_name = "bridge_structure_basic.iab"
        insts_file_name  = "bridge_structure_insts.ial"
        runner           = checker.InstalCheckRunner([ BridgeStructureChecker() ])
        parser           = InstalPyParser()

        bridge_text = data_path.joinpath(bridge_file_name).read_text()
        bridge_data = parser.parse_bridge(bridge_text, parse_source=bridge_file_name)

        insts_text  = data_path.joinpath(insts_file_name).read_text()
        insts_data  = parser.parse_institution(insts_text, parse_source=insts_file_name)

        self.assertEqual(len(bridge_data), 1)
        self.assertEqual(len(insts_data), 2)

        result = runner.check(bridge_data + insts_data)
        self.assertFalse(result)

    def test_basic_fail(self):
        """
        Check a basic bridge + source + sink doesn't report
        """
        bridge_file_name = "bridge_structure_basic.iab"
        runner           = checker.InstalCheckRunner([ BridgeStructureChecker() ])
        parser           = InstalPyParser()

        bridge_text = data_path.joinpath(bridge_file_name).read_text()

        bridge_data = parser.parse_bridge(bridge_text, parse_source=bridge_file_name)

        self.assertEqual(len(bridge_data), 1)

        result = runner.check(bridge_data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 2)
        msgs = {x.msg for x in result[logmod.WARNING]}
        self.assertIn("Bridge Source declared but not defined", msgs)
        self.assertIn("Bridge Sink declared but not defined", msgs)



if __name__ == '__main__':
    unittest.main()
