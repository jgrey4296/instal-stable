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

    def test_fluent_conflict(self):
        runner = checker.InstalCheckRunner([ NameDuplicationCheck() ])

        text = data_path.joinpath("name_duplication_test1.ial").read_text()
        data = InstalPyParser().parse_institution(text, parse_source="name_duplication_test1.ial")
        self.assertIsInstance(data[0], iAST.InstitutionDefAST)

        with self.assertRaises(Exception) as cm:
            runner.check(data)

        the_exc = cm.exception
        self.assertIn(logmod.ERROR, the_exc.args[1])
        self.assertTrue(the_exc.args[1][logmod.ERROR])
        self.assertEqual(the_exc.args[1][logmod.ERROR][0].msg,
                         "Duplicate Fluent Declaration")

if __name__ == '__main__':
    unittest.main()
