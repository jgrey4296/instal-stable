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
test_files      = files("instal.__tests.model_logic.__data")
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


class TestInstalPrelude(unittest.TestCase):
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

    def test_prelude_success(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_inst.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = [] # parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        self.assertEqual(len(solver.results), 1)
        save_last(compiled, solver.results[0].atoms)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalInst)", result)

    def test_prelude_fail(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_inst.ial"], with_prelude=False)
        # Add an event
        parser   = InstalPyParser()
        query    = [] # parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled)
        self.assertEqual(len(solver.results), 0)



##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
