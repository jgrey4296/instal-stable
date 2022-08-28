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

import instal.parser.parse_funcs as dsl
import instal.interfaces.ast as ASTs
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionParser(InstalParserTestCase):
    def test_simple_query(self):
        self.assertParseResultsIsInstance(dsl.top_query,
                                          ("observed person(bob) in greeting", ASTs.QueryTotalityAST),
                                          ("observed afact in greeting",       ASTs.QueryTotalityAST),

                                          )

    def test_query_results(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed person(bob) in greeting", 1, ["bob"]),
                                                   ("""observed person(bob) in greeting\nobserved person(bill, jill) in greeting""", 2, ["bob", "bill", "jill"])
                                                   ):
            match data:
                case text, length, terms:
                    self.assertEqual(len(result[0]), length)
                    for term in result[0].body:
                        self.assertAllIn((x.value for x in term.head.params), terms)

    def test_query_at_time(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed person(bob) in greeting at 5",   5),
                                                   ("observed person(bob) in greeting at 2",   2),
                                                   ("observed person(bob) in greeting at 10",  10),
                                                   ("observed person(bob) in greeting at 1",   1),
                                                   ("observed person(bob) in greeting at 100", 100),
                                                   ):
            self.assertEqual(result[0].body[0].time, data[1])


if __name__ == '__main__':
    unittest.main()
