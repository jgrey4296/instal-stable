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

from clingo import parse_term
from instal.trace.clingo_symbol_state import InstalClingoState
from instal.interfaces import ast as iast
##-- end imports

logging = logmod.root

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestClingoState(unittest.TestCase):
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


    def test_state_creation(self):
        state = InstalClingoState()

        self.assertEqual(state.timestep, 0)


    def test_state_insert(self):
        term1 = parse_term("blah(test,0)")

        state = InstalClingoState()

        self.assertFalse(bool(state.rest))
        state.insert(term1)
        self.assertTrue(bool(state.rest))

    def test_state_contains_int_timesteps(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(test,0)")

        state = InstalClingoState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertIn(term2, state)

    def test_state_contains_nested(self):
        term_a = parse_term("holdsat(blah(test,0),0)")
        term_b = parse_term("holdsat(blah(test,0),0)")

        state = InstalClingoState()

        self.assertNotIn(term_b, state)
        state.insert(term_a)
        self.assertIn(term_b, state)


    def test_state_contains_fail(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(not,0)")

        state = InstalClingoState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertNotIn(term2, state)


    def test_state_contains_force_timestep(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(test,1)")

        state = InstalClingoState()
        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertIn(term2, state)

    def test_state_contains_force_timestep_fail(self):
        term1 = parse_term("blah(test,0)")
        term2 = parse_term("blah(not,1)")

        state = InstalClingoState()

        self.assertNotIn(term2, state)
        state.insert(term1)
        self.assertNotIn(term2, state)


    def test_ast_term(self):
        term_par1 = iast.TermAST("test")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")
        state     = InstalClingoState()

        state.insert(c_term)
        self.assertIn(term1, state)


    def test_ast_term_fail(self):
        term_par1 = iast.TermAST("not")
        term1     = iast.TermAST("blah", [term_par1, iast.TermAST(0)])
        c_term    = parse_term("blah(test,0)")
        state     = InstalClingoState()

        state.insert(c_term)
        self.assertNotIn(term1, state)



##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
