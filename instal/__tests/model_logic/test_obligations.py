#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

#
import logging as logmod
import pathlib
import unittest
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.cli.compiler import compile_target
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.parser.v2.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver

##-- end imports

##-- data
test_files      = files("instal.__data.test_files.minimal")
##-- end data

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

logging = logmod.root

def save_last(compiled, append=None):
    "A utility to save lines of text to a file for debugging compiled output "
    with open(pathlib.Path(__file__).parent / "last_run.lp", 'w') as f:
        f.write("\n".join(compiled))
        if bool(append):
            f.write("\n".join(str(x) for x in append))


class TestInstalObligations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.root
        logging.setLevel(logmod.NOTSET)
        logging.addHandler(cls.file_h)


    @classmethod
    def tearDownClass(cls):
        logging.removeHandler(cls.file_h)

    def test_initial(self):
        pass


if __name__ == '__main__':
    unittest.main()
