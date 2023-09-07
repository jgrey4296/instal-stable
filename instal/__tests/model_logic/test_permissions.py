#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

#
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
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.parser.v2.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver

##-- data
test_files      = files("instal.__tests.model_logic.__data")
##-- end data

logging = logmod.root

def save_last(compiled, append=None):
    "A utility to save lines of text to a file for debugging compiled output "
    with open(pathlib.Path(__file__).parent / "last_run.lp", 'w') as f:
        f.write("\n".join(compiled))
        if bool(append):
            f.write("\n".join(str(x) for x in append))

class TestInstalPermissions:

    def test_event_recognition_unempowered(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_permissions_unempowered.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEvent at 0")
        # Solve
        save_last(compiled)
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query)
        assert((len(solver.results) == 1)
        save_last(compiled, solver.results[0].atoms)
        result = str(solver.results[0].shown)
        assert("institution(minPerUnPow)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("occurred(_unempoweredEvent(basicEvent_i),minPerUnPow,0)" in result)
        assert("occurred(basicEvent_i,minPerUnPow,0)" not in result)
        assert("occurred(_unpermittedEvent(basicEvent_i),minPerUnPow,0)" not in result)

    def test_event_recognition_unpermitted(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_permissions_unpermitted.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEvent at 0.")
        # Solve
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        assert((len(solver.results) == 1)
        result = str(solver.results[0].shown)
        save_last(compiled, solver.results[0].atoms)

        assert("institution(minPerUnPer)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("occurred(_unpermittedEvent(basicEvent_i),minPerUnPer,0)" in result)
        assert("occurred(violation(basicEvent_i),minPerUnPer,0)" in result)

    def test_event_recognition_permitted(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_permissions_permitted.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query)
        assert((len(solver.results) == 1)
        save_last(compiled, solver.results[0].atoms)
        result = str(solver.results[0].shown)
        assert("institution(minPerAllowed)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("occurred(basicEvent_i,minPerAllowed,0)" in result)
