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

import instal.parser.v2.parse_funcs as dsl
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
                                          ("observed person(bob)", ASTs.QueryAST),
                                          ("observed afact",       ASTs.QueryAST),

                                          )

    def test_query_results(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed person(bob)", 1, ["bob"]),
                                                   ("""observed person(bob)\nobserved person(bill, jill)""", 2, ["bob", "bill", "jill"])
                                                   ):
            match data:
                case text, length, terms:
                    self.assertEqual(len(result), length)
                    for term in result:
                        self.assertAllIn((x.value for x in term.head.params), terms)

    def test_query_at_time(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed person(bob) at 5",   5),
                                                   ("observed person(bob) at 2",   2),
                                                   ("observed person(bob) at 10",  10),
                                                   ("observed person(bob) at 1",   1),
                                                   ("observed person(bob) at 100", 100),
                                                   ):
            self.assertEqual(result[0].time, data[1])

    def test_query_multiple_at_time(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed person(bob) at 5\nobserved person(bill) at 10", 5, 10),
                                                   ("observed basicExEvent(first) at 0\nobserved basicExEvent(second)  at 1", 0, 1)
                                                   ):
            self.assertEqual(result[0].time, data[1])
            self.assertEqual(result[1].time, data[2])


##-- ifmain
if __name__ == '__main__':
    unittest.main()
##-- end ifmain
