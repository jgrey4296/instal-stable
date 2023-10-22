#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
import instal.interfaces.ast as ASTs
import instal.parser.v1a.parse_funcs as dsl
from instal.interfaces.parser import InstalParserTestCase

##-- data
data_path = files("instal.parser.v1a.__tests.__data")
##-- end data

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
                assert(link.head.value == desc[0])
                assert(link.link_type == desc[1])


    def test_types(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\ntype Test;\ntype Other;", ["Test", "Other"])
                                                   ):
            types = (x.head.value for x in result[0].types)
            assert(all(x in data[1] for x in types))

    def test_events(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nexogenous event blah;\nexogenous event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),

                                                   ("institution test;\ninst event blah;\ninst event other;\ninst event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),

                                                   ("institution test;\nviolation event blah;\nviolation event other;\nviolation event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ):
            events = result[0].events
            assert(all(x.head.value in data[1] for x in events))
            assert(all(x.annotation for x in events), data[2]))


    def test_fluents(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nfluent testFluent;\nfluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.inertial}),

                                                   ("institution test;\nnoninertial fluent testFluent;\nnoninertial fluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.transient}),

                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation);", ["obFluent"], {ASTs.FluentEnum.obligation}),

                                                   ("institution test;\ncross fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ):

            fluents = result[0].fluents
            assert(all((x.head.value in data[1] for x in fluents))
            assert(all((x.annotation in data[2] for x in fluents))

    def test_generation_rules(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething initiates else;", ["something"], ["else"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test;\nsomething generates else;", ["something"], ["else"], {ASTs.RuleEnum.generates}),
                                                   ):
            rules = result[0].rules
            assert(all(x.head.value in data[1] for x in rules))
            assert(all(y.value in data[2] for x in rules for y in x.body))
            assert(all(x.annotation in data[3] for x in rules))

    def test_transient_rules(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ):
            transients = result[0].rules
            assert(all(str(y) in data[1] for x in transients for y in x.body))
            assert(all(str(y.head) in data[2] for x in transients for y in x.conditions))


    def test_initially(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\ninitially something;", ["something"]),
                                                   ):
            initial = result[0].initial
            assert(all(y.value in data[1] for x in initial for y in x.body))


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
            assert(len(result_list) == len(data[1]))
            for resultCond, expectedCond in zip(result_list, data[1]):
                assert(resultCond.head     == expectedCond.head)
                assert(resultCond.negated  == expectedCond.negated)
                assert(resultCond.operator == expectedCond.operator)
                assert(resultCond.rhs      == expectedCond.rhs)

    def test_rule_with_condition_parsing(self):
        for result, data in self.yieldParseResults(dsl.RULE,
                                                   ("anEv generates someFluent if testVal;", ASTs.GenerationRuleAST, [ASTs.ConditionAST(ASTs.TermAST("testVal"))]),
                                                   ("anEv initiates someFluent if testVal;", ASTs.InertialRuleAST, [ASTs.ConditionAST(ASTs.TermAST("testVal"))]),
                                                   ):
            the_rule = result[:][0]
            assert(isinstance(the_rule, ASTs.RuleAST))
            assert(isinstance(the_rule, data[1]))
            assert(isinstance(the_rule.conditions, list))
            assert(len(the_rule.conditions) == len(data[2]))
            for resultCond, expectedCond in zip(the_rule.conditions, data[2]):
                assert(isinstance(resultCond, ASTs.ConditionAST))
                assert((resultCond.head    == expectedCond.head)
                assert(resultCond.negated  == expectedCond.negated)
                assert(resultCond.operator == expectedCond.operator)
                assert(resultCond.rhs      == expectedCond.rhs)


    def test_simple_full(self):
        self.assertFilesParse(dsl.top_institution,
                              "test_inst.ial",
                              "test_inst2.ial",
                              "test_inst3.ial",
                              loc=data_path)
