#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

import instal.interfaces.ast as ASTs
import instal.parser.v1a.parse_funcs as dsl
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- data
data_path = files("instal.parser.v1a.__tests.__data")
##-- end data

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionParser(InstalParserTestCase):
    def test_simple_institution(self):
        self.assertParseResultsIsInstance(dsl.top_institution,
                                          ("institution simple;\ntype Test;", ASTs.InstitutionDefAST),
                                          )

    def test_simple_bridge(self):
        self.assertParseResultsIsInstance(dsl.top_bridge,
                                          ("bridge test;\ntype Test;\nsink blah;", ASTs.BridgeDefAST),
                                          )


    def test_bridge_links(self):
        for result, data in self.yieldParseResults(dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsink   bloo;\nsource other;", [("bloo", ASTs.BridgeLinkEnum.sink),
                                                                                                              ("other", ASTs.BridgeLinkEnum.source)]),
                                                   ):
            for link, desc in zip(sorted(result[0].links, key=lambda x: x.head.value), data[1]):
                self.assertEqual(link.head.value, desc[0])
                self.assertEqual(link.link_type, desc[1])


    def test_types(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\ntype Test;\ntype Other;", ["Test", "Other"])
                                                   ):
            types = (x.head.value for x in result[0].types)
            self.assertAllIn(types, data[1])

    def test_events(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nexogenous event blah;\nexogenous event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),

                                                   ("institution test;\ninst event blah;\ninst event other;\ninst event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),

                                                   ("institution test;\nviolation event blah;\nviolation event other;\nviolation event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ):
            events = result[0].events
            self.assertAllIn((x.head.value for x in events), data[1])
            self.assertAllIn((x.annotation for x in events), data[2])


    def test_fluents(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nfluent testFluent;\nfluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.inertial}),

                                                   ("institution test;\nnoninertial fluent testFluent;\nnoninertial fluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.transient}),

                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation);", ["obFluent"], {ASTs.FluentEnum.obligation}),

                                                   ("institution test;\ncross fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ):

            fluents = result[0].fluents
            self.assertAllIn((x.head.value for x in fluents), data[1])
            self.assertAllIn((x.annotation for x in fluents), data[2])

    def test_generation_rules(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething initiates else;", ["something"], ["else"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test;\nsomething generates else;", ["something"], ["else"], {ASTs.RuleEnum.generates}),
                                                   ):
            rules = result[0].rules
            self.assertAllIn((x.head.value for x in rules), data[1])
            self.assertAllIn((y.value for x in rules for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in rules), data[3])

    def test_transient_rules(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ):
            transients = result[0].rules
            self.assertAllIn((x.head.value for x in transients), data[1])
            self.assertAllIn((y.value for x in transients for y in x.body), data[2])


    def test_initially(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\ninitially something;", ["something"]),
                                                   ):
            initial = result[0].initial
            self.assertAllIn((y.value for x in initial for y in x.body), data[1])


    def test_condition_parsing(self):
        for result, data in self.yieldParseResults(dsl.CONDITIONS,
                                                   ("testVal", [ASTs.ConditionAST(ASTs.TermAST("testVal"))]),
                                                   ("testVal, testSecond", [ASTs.ConditionAST(ASTs.TermAST("testVal")),
                                                                            ASTs.ConditionAST(ASTs.TermAST("testSecond"))]),
                                                   ("testVal = testOther", [ASTs.ConditionAST(ASTs.TermAST("testVal"),
                                                                                              operator="=",
                                                                                              rhs=ASTs.TermAST("testOther"))]),
                                                   ("testVal < testOther", [ASTs.ConditionAST(ASTs.TermAST("testVal"),
                                                                                              operator="<",
                                                                                              rhs=ASTs.TermAST("testOther"))]),
                                                   ("testVal <= testOther", [ASTs.ConditionAST(ASTs.TermAST("testVal"),
                                                                                               operator="<=",
                                                                                               rhs=ASTs.TermAST("testOther"))])
                                                   ):
            result_list = result[:]
            self.assertEqual(len(result_list), len(data[1]))
            for resultCond, expectedCond in zip(result_list, data[1]):
                self.assertEqual(resultCond.head, expectedCond.head)
                self.assertEqual(resultCond.negated, expectedCond.negated)
                self.assertEqual(resultCond.operator, expectedCond.operator)
                self.assertEqual(resultCond.rhs, expectedCond.rhs)

    def test_rule_with_condition_parsing(self):
        for result, data in self.yieldParseResults(dsl.RULE,
                                                   ("anEv generates someFluent if testVal;", ASTs.GenerationRuleAST, [ASTs.ConditionAST(ASTs.TermAST("testVal"))]),
                                                   ("anEv initiates someFluent if testVal;", ASTs.InertialRuleAST, [ASTs.ConditionAST(ASTs.TermAST("testVal"))]),
                                                   ):
            the_rule = result[:][0]
            self.assertIsInstance(the_rule, ASTs.RuleAST)
            self.assertIsInstance(the_rule, data[1])
            self.assertIsInstance(the_rule.conditions, list)
            self.assertEqual(len(the_rule.conditions), len(data[2]))
            for resultCond, expectedCond in zip(the_rule.conditions, data[2]):
                self.assertIsInstance(resultCond, ASTs.ConditionAST)
                self.assertEqual(resultCond.head, expectedCond.head)
                self.assertEqual(resultCond.negated, expectedCond.negated)
                self.assertEqual(resultCond.operator, expectedCond.operator)
                self.assertEqual(resultCond.rhs, expectedCond.rhs)


    def test_simple_full(self):
        self.assertFilesParse(dsl.top_institution,
                              "test_inst.ial",
                              "test_inst2.ial",
                              "test_inst3.ial",
                              loc=data_path)


if __name__ == '__main__':
    unittest.main()
