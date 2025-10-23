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


class TestInstalPrelude:

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
        assert((len(solver.results) == 1)
        save_last(compiled, solver.results[0].atoms)
        result = str(solver.results[0].shown)
        assert("institution(minimalInst)" in result)

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
        assert((len(solver.results) == 0)
