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
from instal.trace.ast_state import InstalASTState
from instal.interfaces import ast as iast
from instal.parser.v2.utils import TERM
from clingo import parse_term
##-- end imports

logging = logmod.root


class TestASTState:

    def test_initial(self):
        pass



    def test_term_equality(self):
        term1 = iast.TermAST("test")
        term2 = iast.TermAST("test")

        assert(term1 == term2)

    def test_term_inequality(self):
        term1 = iast.TermAST("test")
        term2 = iast.TermAST("nottest")

        assert(term1 != term2)

    def test_term_param_equality(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1])
        term2 = iast.TermAST("blah", [term_par2])

        assert(term1 == term2)

    def test_term_param_inequality(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("nottest")

        term1 = iast.TermAST("blah", [term_par1])
        term2 = iast.TermAST("blah", [term_par2])

        assert(term1 != term2)


    def test_state_creation(self):
        state = InstalASTState()

        assert(state.timestep == 0)


    def test_state_insert(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])

        state = InstalASTState()

        assert(not bool(state.rest))
        state.insert(term1)
        assert(bool(state.rest))

    def test_state_contains_int_timesteps(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        state = InstalASTState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 in state)

    def test_state_contains_nested(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        term_a = iast.TermAST("holdsat", [term1, iast.TermAST(0)])
        term_b = iast.TermAST("holdsat", [term1, iast.TermAST(0)])

        state = InstalASTState()

        assert(term_b not in state)
        state.insert(term_a)
        assert(term_b in state)


    def test_state_contains_fail(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("not")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        state = InstalASTState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 not in state)


    def test_state_contains_force_timestep(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(1)])
        term1_clone  = iast.TermAST(term2.value, term2.params[:-1] + [iast.TermAST(0)])

        assert(term1 == term1_clone)
        state = InstalASTState()
        assert(term2 not in state)
        state.insert(term1)
        assert(term2 in state)

    def test_state_contains_force_timestep_fail(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("nottest")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(1)])

        state = InstalASTState()

        assert(term2 not in state)
        state.insert(term1)
        assert(term2 not in state)


    def test_clingo_term(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")

        state = InstalASTState()

        state.insert(term1)
        assert(c_term in state)

    def test_clingo_term_not_in(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(other,0)")

        state = InstalASTState()

        state.insert(term1)
        assert(c_term not in state)



    def test_to_json(self):
        term1     = TERM.parse_string("observed(else,0)")[0]
        term2     = TERM.parse_string("occurred(something,inst,0)")[0]
        term3     = TERM.parse_string("holdsat(perm(action,role),inst,0)")[0]

        state = InstalASTState()

        state.insert(term1)
        state.insert(term2)
        state.insert(term3)

        as_json = state.to_json()
        assert(isinstance(as_json, dict))
        assert(all([x in as_json for x in ["timestep", "occurred", "observed", "holdsat", "rest"]]))

        assert(as_json["timestep"] == 0)
        assert(as_json["observed"][0] == "observed(else,0)")
        assert(as_json["occurred"][0] == "occurred(something,inst,0)")
        assert(as_json["holdsat"]["perm"][0] == "holdsat(perm(action,role),inst,0)")
