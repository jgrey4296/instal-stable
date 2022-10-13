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
            f.write("\n%% Resulting Atoms:\n ")
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
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("initially testFact in minimalFluents")
        query     = []
        # Solve
        self.assertTrue(compiled)
        self.assertTrue(situation)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalFluents)", result)
        self.assertIn("holdsat(testFact,minimalFluents,0)", result)

    def test_minimal_fluent_negated(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("not initially testFact in minimalFluents")
        query     = []
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalFluents)", result)
        self.assertNotIn("holdsat(testFact,minimalFluents,0)", result)

    def test_minimal_fluent_initiate(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("not initially testFact in minimalFluents")
        query     = parser.parse_query("observed basicEvent(init) at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalFluents)", result)
        self.assertIn("holdsat(perm(basicInstEvent(init)),minimalFluents,0)", result)
        # Starts off not holding
        self.assertNotIn("holdsat(testFact,minimalFluents,0)", result)
        # initiation happens
        self.assertIn("observed(basicEvent(init),1)", result)
        self.assertIn("occurred(basicInstEvent(init),minimalFluents,1)", result)
        # next time step, fact holds
        self.assertIn("holdsat(testFact,minimalFluents,2)", result)

    def test_minimal_fluent_propagation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("not initially testFact in minimalFluents")
        query     = parser.parse_query("observed basicEvent(init) at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=5'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalFluents)", result)
        self.assertIn("holdsat(perm(basicInstEvent(init)),minimalFluents,0)", result)
        # Starts off not holding
        self.assertNotIn("holdsat(testFact,minimalFluents,0)", result)
        # Once it does,
        self.assertIn("holdsat(testFact,minimalFluents,2)", result)
        # It continues holding
        self.assertIn("holdsat(testFact,minimalFluents,3)", result)
        self.assertIn("holdsat(testFact,minimalFluents,4)", result)
        self.assertIn("holdsat(testFact,minimalFluents,5)", result)



    def test_minimal_fluent_terminate(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("initially testFact in minimalFluents")
        query     = parser.parse_query("observed basicEvent(term) at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalFluents)", result)
        # Initially holds:
        self.assertIn("holdsat(perm(basicInstEvent(term)),minimalFluents,0)", result)
        self.assertIn("holdsat(testFact,minimalFluents,0)", result)
        # termination happens:
        self.assertIn("occurred(basicInstEvent(term),minimalFluents,1)", result)
        # not longer holds on the next step
        self.assertNotIn("holdsat(testFact,minimalFluents,2)", result)



if __name__ == '__main__':
    unittest.main()
