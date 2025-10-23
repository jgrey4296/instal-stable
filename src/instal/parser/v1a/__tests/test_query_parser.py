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
import instal.parser.v1a.parse_funcs as dsl
import instal.interfaces.ast as ASTs
from instal.interfaces.parser import InstalParserTestCase


class TestInstitutionParser(InstalParserTestCase):
    def test_simple_query(self):
        self.assertParseResultsIsInstance(dsl.top_query,
                                          ("observed(person(bob))", ASTs.QueryAST),
                                          ("observed(afact)",       ASTs.QueryAST),

                                          )

    def test_query_results(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed(person(bob), inst)", 1, ["bob"]),
                                                   ("""observed(person(bob))\nobserved(person(bill, jill))""", 2, ["bob", "bill", "jill"])
                                                   ):
            match data:
                case text, length, terms:
                    assert(len(result) == length)
                    for term in result:
                        assert(all(x.value in terms for x in term.head.params))
