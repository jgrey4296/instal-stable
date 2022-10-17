#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

from dataclasses import replace
import logging as logmod
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from clingo import Control, parse_term, Function, Number
from instal.solve.clingo_solver import ClingoSolver
import instal.interfaces.solver as iSolve
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

logging = logmod.root

class TestInstalClingoSolver(unittest.TestCase):
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
        solver = ClingoSolver()
        self.assertIsInstance(solver, ClingoSolver)

    def test_solver_initialisation(self):
        solver = ClingoSolver()
        self.assertIsNotNone(solver.ctl)

    def test_solver_with_init_options(self):
        solver = ClingoSolver(options=['-n', 2, '-c', "horizon=2"])
        self.assertIsInstance(solver, ClingoSolver)

    def test_basic_model(self):
        solver = ClingoSolver("a. b. c. d. e :- a, b, c.")
        result = solver.solve()
        self.assertEqual(result, 1)

    def test_basic_model_result(self):
        solver = ClingoSolver("a. b. c. d. e :- a, b, c.")
        count = solver.solve()
        self.assertEqual(count, 1)
        model = solver.results[0]
        self.assertIsInstance(model,iSolve.InstalModelResult)
        self.assertTrue(all([str(x) in {"a","b","c","d","e"} for x in model.atoms]))

    def test_basic_fail(self):
        # Leaving off the final `.`
        with self.assertRaises(RuntimeError):
            solver = ClingoSolver("a. b. c. d. e :- a, b, c")

    def test_assertion_assignment(self):
        term   = parse_term("testVal")
        term_2 = parse_term("a")
        solver = ClingoSolver("#external testVal. a.")
        count  = solver.solve(["testVal"])
        self.assertEqual(count, 1)

        self.assertIn(term, solver.results[0].atoms)
        self.assertIn(term_2, solver.results[0].atoms)

    def test_assertion_assignment_false(self):
        term   = parse_term("testVal")
        term_2 = parse_term("a")
        solver = ClingoSolver("#external testVal. a.")
        count  = solver.solve()
        self.assertEqual(count, 1)

        self.assertNotIn(term, solver.results[0].atoms)
        self.assertIn(term_2, solver.results[0].atoms)

    def test_force_fresh(self):
        term   = parse_term("testVal")
        term_2 = parse_term("a")
        solver = ClingoSolver("#external testVal. a.")
        count  = solver.solve(["testVal"])

        self.assertEqual(count, 1)
        self.assertIn(term, solver.results[0].atoms)
        self.assertIn(term_2, solver.results[0].atoms)
        count2 = solver.solve(fresh=True)
        self.assertEqual(count, 1)
        self.assertEqual(len(solver.results),1)
        self.assertNotIn(term, solver.results[0].atoms)
        self.assertIn(term_2, solver.results[0].atoms)


    def test_multishot_no_change(self):
        term   = parse_term("testVal")
        term_2 = parse_term("a")
        solver = ClingoSolver("#external testVal. a.")
        count  = solver.solve([ term ])

        self.assertEqual(count, 1)
        self.assertIn(term, solver.results[0].atoms)
        self.assertIn(term_2, solver.results[0].atoms)

        count2 = solver.solve()
        self.assertEqual(len(solver.results),2)
        self.assertEqual(count, 1)
        self.assertIn(term, solver.results[-1].atoms)
        self.assertIn(term_2, solver.results[-1].atoms)


    def test_multishot_with_change(self):
        term         = parse_term("testVal(1)")
        term_2       = parse_term("testVal(2)")
        a_term       = parse_term("a")
        solver = ClingoSolver("#external testVal(1..3). a.")
        count  = solver.solve([term])

        self.assertEqual(count, 1)
        self.assertIn(term, solver.results[0].atoms)
        self.assertIn(a_term, solver.results[0].atoms)

        # change the value of the term:
        count2 = solver.solve([term_2, term])
        self.assertEqual(count, 1)
        self.assertNotIn(str(term), solver.results[-1].atoms)
        self.assertIn(term_2, solver.results[-1].atoms)
        self.assertIn(a_term, solver.results[-1].atoms)


    def test_multishot_incremental(self):
        solver = ClingoSolver("""
        #program base.
        on(X, 0) :- init_on(X).
        init_on(a).
        disc(a;b;c).

        #program step(t).
        1 { move(D,t) : disc(D) } 1.

        on(X, t) :- move(X,t).
        """)
        count  = solver.solve()
        self.assertEqual(count, 1)

        # change the value of the term:
        solver.solve(reground=[("step", [Number(1)])])
        solver.solve(reground=[("step", [Number(5)])])
        solver.solve(reground=[("step", [Number(10)])])
        self.assertTrue(True)


    def test_file_load(self):
        solver = ClingoSolver([])

    def test_metadata(self):
        pass

if __name__ == '__main__':
    unittest.main()
