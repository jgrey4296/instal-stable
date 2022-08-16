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

from instal.interfaces.parser import InstalParserTestCase
from instal.parser.pyparse_institution import TERM
import instal.interfaces.ast as ASTs
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestTermParser(InstalParserTestCase):

    def test_simple_term(self):
        self.assertParseResults(TERM,
                                ("basic",                            ASTs.TermAST("basic")),
                                ("other",                            ASTs.TermAST("other")),
                                # Params
                                ("basic(aParam)",                    ASTs.TermAST("basic", [ASTs.TermAST("aParam")])),
                                ("basic(aParam, another)",           ASTs.TermAST("basic", [ASTs.TermAST("aParam"), ASTs.TermAST("another")])),
                                ("manyParams(a,b,c,d,e,f,g,h,i,j)",  ASTs.TermAST("manyParams", [ASTs.TermAST(x) for x in "abcdefghij"])),
                                # Variables
                                ("Var",                              ASTs.TermAST("Var", is_var=True)),
                                ("test(ParamA, paramB)",             ASTs.TermAST("test", [ ASTs.TermAST("ParamA", is_var=True), ASTs.TermAST("paramB")])),
                                # Nesting:
                                ("basic(other, another(nested, even(further)))",
                                 ASTs.TermAST("basic", params=[ASTs.TermAST("other"),
                                                               ASTs.TermAST("another",
                                                                            params=[ASTs.TermAST("nested"),
                                                                                    ASTs.TermAST("even",
                                                                                                 params=[ASTs.TermAST("further")])])]))

                                )


    def test_fail_term(self):
        self.assertParserFails(TERM,
                               ("basicFail@",         9),
                               ("basic@Fail",         5),
                               ("basic(",             5),
                               ("underscore_test",    10),
                               # Fails at the ( after backtracking, not at the _:
                               ("paramFail(a_b, cd)", 9)
                               )

    def test_simple_yield(self):
        for result, vals in self.yieldParseResults(TERM,
                                                   ("basic", "basic"),
                                                   ("other", "other")
                                                   ):
            self.assertIsInstance(result[0], ASTs.TermAST)
            self.assertEqual(result[0].value, vals[1])

if __name__ == '__main__':
    unittest.main()
