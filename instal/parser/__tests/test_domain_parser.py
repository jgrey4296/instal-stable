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

import instal.parser.pyparse_institution as dsl
import instal.interfaces.ast as ASTs
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestDomainParser(InstalParserTestCase):

    def test_simple_domain_spec(self):
        self.assertParseResultsIsInstance(dsl.top_domain,
                                          ("Agent: alice", ASTs.DomainTotalityAST),
                                          )

    def test_domain_results(self):
        for result, data in self.yieldParseResults(dsl.top_domain,
                                                   {"text": "Agent: alice", "length": 1, "type_name": "Agent", "values": ["alice"]},
                                                   ("People: alice bob", 1, "People", ["alice", "bob"]),
                                                   ("""Agent: bill\nPeople: alice bob""", 2, ["Agent", "People"], ["alice", "bob", "bill"])

                                                 ):
            match data:
                case dict():
                    self.assertEqual(len(result[0]), data['length'])
                    for spec in result[0].body:
                        self.assertIsInstance(spec, ASTs.DomainSpecAST)
                        self.assertEqual(spec.head.value, data['type_name'])
                        self.assertAllIn((x.value for x in spec.body), data['values'])
                case text, length, type_names, values if isinstance(type_names, list):
                    self.assertEqual(len(result[0]), length)
                    for spec in result[0].body:
                        self.assertIsInstance(spec, ASTs.DomainSpecAST)
                        self.assertIn(spec.head.value, type_names)
                        self.assertAllIn((x.value for x in spec.body), values)

                case text, length, type_name, values:
                    self.assertEqual(len(result[0]), length)
                    for spec in result[0].body:
                        self.assertIsInstance(spec, ASTs.DomainSpecAST)
                        self.assertEqual(spec.head.value, type_name)
                        self.assertTrue(all(x.value in values for x in spec.body))





if __name__ == '__main__':
    unittest.main()
