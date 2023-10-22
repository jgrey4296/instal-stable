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

class TestDomainParser(InstalParserTestCase):

    def test_simple_domain_spec(self):
        self.assertParseResultsIsInstance(dsl.top_domain,
                                          ("Agent: alice", ASTs.DomainSpecAST)
                                          )

    def test_domain_results(self):
        for result, data in self.yieldParseResults(dsl.top_domain,
                                                   {"text": "Agent: alice", "length": 1, "type_name": "Agent", "values": ["alice"]},
                                                   ("People: alice bob", 1, "People", ["alice", "bob"]),
                                                   ("""Agent: bill\nPeople: alice bob""", 2, ["Agent", "People"], ["alice", "bob", "bill"])

                                                 ):
            match data:
                case dict():
                    assert(len(result) ==  data['length'])
                    for spec in result:
                        assert(isinstance(spec, ASTs.DomainSpecAST))
                        assert(spec.head.value ==  data['type_name'])
                        assert((x.value for x in spec.body) in data['values'])

                case text, length, type_names, values if isinstance(type_names, list):
                    assert(len(result) ==  length)
                    for spec in result:
                        assert(isinstance(spec, ASTs.DomainSpecAST))
                        assert(spec.head.value in type_names)
                        assert(all(x.value in values for x in spec.body))

                case text, length, type_name, values:
                    assert(len(result) ==  length)
                    for spec in result:
                        assert(isinstance(spec, ASTs.DomainSpecAST))
                        assert(spec.head.value ==  type_name)
                        assert(all(x.value in values for x in spec.body))
