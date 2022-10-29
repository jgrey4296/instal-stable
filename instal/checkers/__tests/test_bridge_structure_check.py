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

    @unittest.skip
    def test_basic_pass(self):
        """
        Check no reports are generated on proper use of events
        """
        file_name = "event_check_pass.ial"
        runner    = checker.InstalCheckRunner([ EventCheck() ])

        text = data_path.joinpath(file_name).read_text()
        data = InstalPyParser().parse_institution(text, parse_source=file_name)
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        result = runner.check(data)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
