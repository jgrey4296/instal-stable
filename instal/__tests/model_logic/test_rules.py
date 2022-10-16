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


class TestInstalGeneration(unittest.TestCase):
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

    def test_simple_generation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventWithParam(first) at 0")
        situation = [] #parser.parse_situation("initially perm(instBasicEvent(first)) in minimalRules")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventWithParam(first),0)", result)
        self.assertIn("occurred(instBasicEvent(first),minimalRules,0)", result)

    def test_simple_generation_var_change(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventWithParam(second) at 0")
        situation = parser.parse_situation("initially perm(instBasicEvent(second)) in minimalRules")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventWithParam(second),0)", result)
        self.assertIn("occurred(instBasicEvent(second),minimalRules,0)", result)




    def test_simple_generation_time_responsive(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventWithParam(first) at 1")
        situation = parser.parse_situation("initially perm(instBasicEvent(first)) in minimalRules")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventWithParam(first),1)", result)
        self.assertIn("occurred(instBasicEvent(first),minimalRules,1)", result)


    def test_event_with_multi_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventMulti(first, second) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventMulti(first,second),0)", result)
        self.assertIn("occurred(instMultiVar(first,first),minimalRules,0)", result)

    def test_event_with_multi_var_double_generation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventMulti(first, second) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventMulti(first,second),0)", result)
        self.assertIn("occurred(instMultiVar(first,first),minimalRules,0)", result)
        self.assertIn("occurred(instMultiVar(second,second),minimalRules,0)", result)



    def test_event_with_chained_generation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventWithParam(first) at 1")
        situation = parser.parse_situation("initially perm(instChainMid(first)) in minimalRules")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventWithParam(first),1)", result)
        self.assertIn("occurred(instChainStart(first),minimalRules,1)", result)
        self.assertIn("occurred(instChainMid(first),minimalRules,1)", result)
        self.assertIn("occurred(instChainEnd(first),minimalRules,1)", result)

    def test_event_with_chained_interrupted(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventWithParam(first) at 1")
        situation = [] #parser.parse_situation("initially perm(instChainMid(first)) in minimalRules")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalRules)", result)
        self.assertIn("observed(basicExEventWithParam(first),1)", result)
        self.assertIn("occurred(instChainStart(first),minimalRules,1)", result)
        self.assertNotIn("occurred(instChainMid(first),minimalRules,1)", result)
        self.assertNotIn("occurred(instChainEnd(first),minimalRules,1)", result)
        self.assertIn("occurred(_unpermittedEvent(instChainMid(first)),minimalRules,1)", result)

    def test_minimal_transient_rule(self):
        """
        Ensure a transient fluent only holds when its condition is met.
        """
        # Compile a harness
        compiled = compile_target([test_files / "minimal_rules.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("not initially testFact in minimalRules\ninitially perm(instBasicEvent(first)) in minimalRules")
        query     = parser.parse_query("observed basicExEventWithParam(first) at 1\nobserved basicExEventWithParam(second) at 3")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=4'])

        # Check it is observed
        solver.solve(query + situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertIn("institution(minimalRules)", result)

        self.assertNotIn("holdsat(testTransient,minimalRules,0)", result)

        self.assertIn("observed(basicExEventWithParam(first),1)", result)
        self.assertIn("occurred(instBasicEvent(first),minimalRules,1)", result)
        self.assertNotIn("holdsat(testTransient,minimalRules,1)", result)

        self.assertIn("holdsat(testFluent,minimalRules,2)", result)
        self.assertIn("holdsat(testTransient,minimalRules,2)", result)

        self.assertIn("observed(basicExEventWithParam(second),3)", result)
        self.assertIn("occurred(instBasicEvent(second),minimalRules,3)", result)
        self.assertIn("holdsat(testFluent,minimalRules,3)", result)
        self.assertIn("holdsat(testTransient,minimalRules,3)", result)

        self.assertNotIn("holdsat(testFluent,minimalRules,4)", result)
        self.assertNotIn("holdsat(testTransient,minimalRules,4)", result)

if __name__ == '__main__':
    unittest.main()
