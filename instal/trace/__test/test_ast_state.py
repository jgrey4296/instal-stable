#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.trace.ast_state import InstalASTState
from instal.interfaces import ast as iast
from instal.parser.v2.utils import TERM
from clingo import parse_term
##-- end imports

logging = logmod.root

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestASTState(unittest.TestCase):
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

    def test_initial(self):
        pass



    def test_term_equality(self):
        term1 = iast.TermAST("test")
        term2 = iast.TermAST("test")

        self.assertEqual(term1, term2)

    def test_term_inequality(self):
        term1 = iast.TermAST("test")
        term2 = iast.TermAST("nottest")

        self.assertNotEqual(term1, term2)

    def test_term_param_equality(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1])
        term2 = iast.TermAST("blah", [term_par2])

        self.assertEqual(term1, term2)

    def test_term_param_inequality(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("nottest")

        term1 = iast.TermAST("blah", [term_par1])
        term2 = iast.TermAST("blah", [term_par2])

        self.assertNotEqual(term1, term2)


    def test_state_creation(self):
        state = InstalASTState()

        self.assertEqual(state.timestep, 0)


    def test_state_insert(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])

        state = InstalASTState()

        self.assertFalse(bool(state.rest))
        state.insert(term1)
        self.assertTrue(bool(state.rest))

    def test_state_contains_int_timesteps(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        state = InstalASTState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertIn(term2, state)

    def test_state_contains_nested(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        term_a = iast.TermAST("holdsat", [term1, iast.TermAST(0)])
        term_b = iast.TermAST("holdsat", [term1, iast.TermAST(0)])

        state = InstalASTState()

        self.assertNotIn(term_b, state)
        state.insert(term_a)
        self.assertIn(term_b, state)


    def test_state_contains_fail(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("not")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(0)])

        state = InstalASTState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertNotIn(term2, state)


    def test_state_contains_force_timestep(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("test")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(1)])
        term1_clone  = iast.TermAST(term2.value, term2.params[:-1] + [iast.TermAST(0)])

        self.assertEqual(term1, term1_clone)
        state = InstalASTState()
        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertIn(term2, state)

    def test_state_contains_force_timestep_fail(self):
        term_par1 = iast.TermAST("test")
        term_par2 = iast.TermAST("nottest")

        term1 = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        term2 = iast.TermAST("blah", [term_par2, iast.TermAST(1)])

        state = InstalASTState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertNotIn(term2, state)


    def test_clingo_term(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")

        state = InstalASTState()

        state.insert(term1)
        self.assertTrue(c_term in state)

    def test_clingo_term_not_in(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(other,0)")

        state = InstalASTState()

        state.insert(term1)
        self.assertFalse(c_term in state)



    def test_to_json(self):
        term1     = TERM.parse_string("observed(else,0)")[0]
        term2     = TERM.parse_string("occurred(something,inst,0)")[0]
        term3     = TERM.parse_string("holdsat(perm(action,role),inst,0)")[0]

        state = InstalASTState()

        state.insert(term1)
        state.insert(term2)
        state.insert(term3)

        as_json = state.to_json()
        self.assertIsInstance(as_json, dict)
        self.assertTrue(all([x in as_json for x in ["timestep", "occurred", "observed", "holdsat", "rest"]]))

        self.assertEqual(as_json["timestep"], 0)
        self.assertEqual(as_json["observed"][0], "observed(else,0)")
        self.assertEqual(as_json["occurred"][0], "occurred(something,inst,0)")
        self.assertEqual(as_json["holdsat"]["perm"][0], "holdsat(perm(action,role),inst,0)")


##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
