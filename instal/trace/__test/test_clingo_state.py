#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from clingo import parse_term
from instal.trace.clingo_symbol_state import InstalClingoState
from instal.interfaces import ast as iast

logging = logmod.root

class TestClingoState:

    def test_state_creation(self):
        state = InstalClingoState()

        assert(state.timestep == 0)

    def test_state_insert(self):
        term1 = parse_term("blah(test,0)")

        state = InstalClingoState()

        assert(not bool(state.rest))
        state.insert(term1)
        assert(bool(state.rest))

    def test_state_contains_int_timesteps(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(test,0)")

        state = InstalClingoState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 in state)

    def test_state_contains_nested(self):
        term_a = parse_term("holdsat(blah(test,0),0)")
        term_b = parse_term("holdsat(blah(test,0),0)")

        state = InstalClingoState()

        assert(term_b not in state)
        state.insert(term_a)
        assert(term_b in state)

    def test_state_contains_fail(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(not,0)")

        state = InstalClingoState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 not in state)

    def test_state_contains_force_timestep(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(test,1)")

        state = InstalClingoState()
        assert(term2 not in state)
        state.insert(term1)
        assert(term2 in state)

    def test_state_contains_force_timestep_fail(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(not,1)")

        state = InstalClingoState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 not in state)

    def test_ast_term(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")
        state     = InstalClingoState()

        state.insert(c_term)
        assert(term1 in state)

    def test_ast_term_fail(self):
        term_par1 = iast.TermAST("not")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")
        state     = InstalClingoState()

        state.insert(c_term)
        assert(term1 not in state)
