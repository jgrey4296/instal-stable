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

from instal.validate.bridge_structure_validator import BridgeStructureValidator
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


class TestBridgeStructureValidator(unittest.TestCase):
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
        runner = validate.InstalValidatorRunner([ BridgeStructureValidator() ])
        self.assertIsInstance(runner, validate.InstalValidatorRunner)
        self.assertIsNotNone(runner.validators)

    def test_basic_pass(self):
        """
        Validator a basic bridge + source + sink doesn't report
        """
        bridge_file_name = data_path / "bridge_structure_basic.iab"
        insts_file_name  = data_path / "bridge_structure_insts.ial"
        runner           = validate.InstalValidatorRunner([ BridgeStructureValidator() ])

        bridge_data = parser.parse_bridge(bridge_file_name)
        insts_data  = parser.parse_institution(insts_file_name)

        self.assertEqual(len(bridge_data), 1)
        self.assertEqual(len(insts_data), 2)

        result = runner.validate(bridge_data + insts_data)
        self.assertFalse(result)

    def test_basic_fail(self):
        """
        Validator a basic bridge + source + sink doesn't report
        """
        bridge_file_name = data_path / "bridge_structure_basic.iab"
        runner           = validate.InstalValidatorRunner([ BridgeStructureValidator() ])

        bridge_data = parser.parse_bridge(bridge_file_name)

        self.assertEqual(len(bridge_data), 1)

        result = runner.validate(bridge_data)
        self.assertTrue(result)
        self.assertIn(logmod.WARNING, result)
        self.assertEqual(len(result[logmod.WARNING]), 2)
        msgs = {x.msg for x in result[logmod.WARNING]}
        self.assertIn("Bridge Source declared but not defined", msgs)
        self.assertIn("Bridge Sink declared but not defined", msgs)



if __name__ == '__main__':
    unittest.main()
