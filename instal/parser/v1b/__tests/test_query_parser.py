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

import instal.parser.v1b.parse_funcs as dsl
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
                                          ("observed(person(bob), inst)", ASTs.QueryAST),
                                          ("observed(afact)",       ASTs.QueryAST),

                                          )

    def test_query_results(self):
        for result, data in self.yieldParseResults(dsl.top_query,
                                                   ("observed(person(bob))", 1, ["bob"]),
                                                   ("""observed(person(bob))\nobserved(person(bill, jill))""", 2, ["bob", "bill", "jill"])
                                                   ):
            match data:
                case text, length, terms:
                    self.assertEqual(len(result), length)
                    for term in result:
                        self.assertAllIn((x.value for x in term.head.params), terms)


##-- ifmain
if __name__ == '__main__':
    unittest.main()

##-- end ifmain
