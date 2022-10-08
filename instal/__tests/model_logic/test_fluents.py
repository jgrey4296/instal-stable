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

from instal.cli.compiler import compile_target
from instal.parser.v2.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver
from instal.defaults import STANDARD_PRELUDE_loc
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

class TestInstalFluents(unittest.TestCase):
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

    def test_minimal_fluent(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluent.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        situation = parser.parse_situation("initially testFact in minimalFluent")
        # query    = parser.parse_query("observed basicExEvent at 0")
        query = []
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalFluent)", result)
        self.assertIn("holdsat(testFact,minimalFluent,0)", result)

    def test_minimal_fluent_negated(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluent.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        situation = parser.parse_situation("not initially testFact in minimalFluent")
        # query    = parser.parse_query("observed basicExEvent at 0")
        query = []
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalFluent)", result)
        self.assertNotIn("holdsat(testFact,minimalFluent,0)", result)

    def test_minimal_fluent_initiate(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluent.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        # situation = parser.parse_situation("not initially testFact in minimalFluent\ninitially perm(basicInstEvent) in minimalFluent")
        situation = parser.parse_situation("not initially testFact in minimalFluent")
        query     = parser.parse_query("observed basicEvent at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalFluent)", result)
        self.assertIn("holdsat(perm(basicInstEvent),minimalFluent,0)", result)
        self.assertNotIn("holdsat(testFact,minimalFluent,0)", result)
        self.assertIn("holdsat(testFact,minimalFluent,2)", result)

    def test_minimal_fluent_terminate(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluent.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("initially testFact in minimalFluent")
        query     = parser.parse_query("observed basicEventTerm at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalFluent)", result)
        self.assertIn("holdsat(perm(basicInstEventTerm),minimalFluent,0)", result)
        self.assertIn("occurred(basicInstEventTerm,minimalFluent,1)", result)
        self.assertIn("holdsat(testFact,minimalFluent,0)", result)
        self.assertNotIn("holdsat(testFact,minimalFluent,2)", result)



if __name__ == '__main__':
    unittest.main()
