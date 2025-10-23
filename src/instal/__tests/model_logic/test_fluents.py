#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest

from instal.cli.compiler import compile_target
from instal.parser.v2.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver
from instal.defaults import STANDARD_PRELUDE_loc

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
            f.write("\n%% Resulting Atoms:\n ")
            f.write("\n".join(str(x) for x in append))

class TestInstalFluents:

    def test_minimal_fluent(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_fluents.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        situation = parser.parse_situation("initially testFact in minimalFluents")
        query     = []
        # Solve
        assert(compiled)
        assert(situation)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query + situation)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalFluents)" in result)
        assert("holdsat(testFact,minimalFluents,0)" in result)

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
        solver.solve(query + situation)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalFluents)" in result)
        assert("holdsat(testFact,minimalFluents,0)" not in result)

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
        solver.solve(query + situation)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        assert("institution(minimalFluents)" in result)
        assert("holdsat(deontic(permitted,basicInstEvent(init)),minimalFluents,0)" in result)
        # Starts off not holding
        assert("holdsat(testFact,minimalFluents,0)" not in result)
        # initiation happens
        assert("observed(basicEvent(init),1)" in result)
        assert("occurred(basicInstEvent(init),minimalFluents,1)" in result)
        # next time step, fact holds
        assert("holdsat(testFact,minimalFluents,2)" in result)

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
        solver.solve(query + situation)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        assert("institution(minimalFluents)" in result)
        assert("holdsat(deontic(permitted,basicInstEvent(init)),minimalFluents,0)" in result)
        # Starts off not holding
        assert("holdsat(testFact,minimalFluents,0)" not in result)
        # Once it does,
        assert("holdsat(testFact,minimalFluents,2)" in result)
        # It continues holding
        assert("holdsat(testFact,minimalFluents,3)" in result)
        assert("holdsat(testFact,minimalFluents,4)" in result)
        assert("holdsat(testFact,minimalFluents,5)" in result)



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
        solver.solve(query + situation)
        assert(len(solver.results)== 1)
        result = str(solver.results[0].shown)
        save_last(compiled, append=solver.results[0].atoms)
        assert("institution(minimalFluents)" in result)
        # Initially holds:
        assert("holdsat(deontic(permitted,basicInstEvent(term)),minimalFluents,0)" in result)
        assert("holdsat(testFact,minimalFluents,0)" in result)
        # termination happens:
        assert("occurred(basicInstEvent(term),minimalFluents,1)" in result)
        # not longer holds on the next step
        assert("holdsat(testFact,minimalFluents,2)" not in result)
