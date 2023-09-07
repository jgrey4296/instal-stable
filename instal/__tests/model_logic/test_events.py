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

class TestInstalEvents:

    def test_event_observation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("observed(null,0)" not in result)

    def test_event_observation_timestep(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEvent,1)" in result)
        assert("observed(null,1)" not in result)

    def test_event_observation_twice(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent \nobserved basicExEvent at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)

        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("observed(basicExEvent,1)" in result)


    def test_event_observation_null_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_inst.ial"], with_prelude=True)
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])
        solver.solve()

        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalInst)" in result)
        assert("observed(null,0)" in result)
        assert("observed(null,1)" in result)
        assert("occurred(null,minimalInst,0)" in result)
        assert("occurred(null,minimalInst,1)" in result)
        assert("occurred(null,minimalInst,2)" in result)
        # null events are generated:
        # assertIn("observed(null,0)", result)


    def test_event_observation_outside_time_bounds(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 10")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        solver.solve(query)

        assert(len(solver.results) == 1)
        result : str = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        # Event is not observed
        assert("observed(basicExEvent,10)" not in result)

    def test_event_observation_inside_extended_time_bounds(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 10")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=15'])

        solver.solve(query)

        assert(len(solver.results) == 1)
        result : str = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        # Event is not observed
        assert("observed(basicExEvent,10)" in result)




    def test_event_observation_different_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent\nobserved secondEvent at 1")
        # Solve
        save_last(compiled)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)

        assert(len(solver.results) == 1)
        result : str = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEvent,0)" in result)
        assert("observed(secondEvent,1)" in result)


    def test_event_observation_with_conflicting_times(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add events
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 0\nobserved secondEvent at 0")
        # Solve
        save_last(compiled)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        solver.solve(query)
        # There is not model for it:
        assert(len(solver.results) == 0)

    def test_event_observation_unrecognised(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed badEvent at 0")
        # Solve
        save_last(compiled)
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(_unrecognisedEvent,0)" in result)

    def test_event_with_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithParam(first) at 0\nobserved basicExEventWithParam(second) at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        ("institution(minimalEvents)" in result)
        ("observed(basicExEventWithParam(first),0)" in result)
        ("observed(basicExEventWithParam(second),1)" in result)
        assert("observed(null,0)" not in result)


    def test_event_with_unrecognized_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithVar(other) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEventWithParam(other),0)" not in result)

    def test_event_with_domain_extended_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithParam(other) at 0")
        domain   = InstalDomainCompiler().compile(parser.parse_domain("Example : other"))
        # Solve
        solver   = ClingoSolver("\n".join(compiled + [domain]),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        assert(len(solver.results) == 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEventWithParam(other),0)" in result)

    def test_event_with_multi_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventMulti(first, second, third) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        assert(len(solver.results) in 1)
        result = str(solver.results[0].shown)
        assert("institution(minimalEvents)" in result)
        assert("observed(basicExEventMulti(first,second,third),0)" in result)
