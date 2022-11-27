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
import instal.parser.v2.bridge_parse_funcs as b_dsl
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- data
data_path = files("instal.parser.v2.__tests.__data")
##-- end data

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionParser(InstalParserTestCase):
    def test_simple_institution(self):
        self.assertParseResultsIsInstance(b_dsl.top_bridge,
                                          ("bridge simple;\ntype Test;", ASTs.InstitutionDefAST),
                                          )

    def test_simple_bridge(self):
        self.assertParseResultsIsInstance(b_dsl.top_bridge,
                                          ("bridge test;\ntype Test;\nsink blah;", ASTs.BridgeDefAST),
                                          )

    def test_bridge_links(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsink   bloo;\nsource other;", [("bloo", ASTs.BridgeLinkEnum.sink),
                                                                                                              ("other", ASTs.BridgeLinkEnum.source)]),
                                                   ):
            for link, desc in zip(sorted(result[0].links, key=lambda x: x.head.value), data[1]):
                self.assertEqual(link.head.value, desc[0])
                self.assertEqual(link.link_type, desc[1])

    def test_types(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\ntype Other;", ["Test", "Other"])
                                                   ):
            types = (x.head.value for x in result[0].types)
            self.assertAllIn(types, data[1])

    def test_events(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\nexogenous event blah;\nexogenous event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),
                                                   ("bridge test;\nexo event blah;\nexo event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),
                                                   ("bridge test;\nexternal event blah;\nexternal event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),

                                                   ("bridge test;\ninstitutional event blah;\ninstitutional event other;\ninstitutional event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),
                                                   ("bridge test;\ninst event blah;\ninst event other;\ninst event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),


                                                   ("bridge test;\nviolation event blah;\nviolation event other;\nviolation event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ("bridge test;\nviol event blah;\nviol event other;\nviol event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ):
            events = result[0].events
            self.assertAllIn((x.head.value for x in events), data[1])
            self.assertAllIn((x.annotation for x in events), data[2])


    def test_fluents(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\nfluent testFluent;\nfluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.inertial}),

                                                   ("bridge test;\ntransient fluent testFluent;\ntransient fluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.transient}),

                                                   ("bridge test;\nobligation fluent obFluent(obligation, deadline, violation, oneshot);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("bridge test;\nobligation fluent obFluent(obligation, deadline, violation, multishot);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("bridge test;\nobl fluent obFluent(obligation, deadline, violation, multishot);", ["obFluent"], {ASTs.FluentEnum.obligation}),

                                                   ("bridge test;\ncross fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ("bridge test;\nx fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ):

            fluents = result[0].fluents
            self.assertAllIn((x.head.value for x in fluents), data[1])
            self.assertAllIn((x.annotation for x in fluents), data[2])

    def test_generation_rules(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\nsomething generates else;", ["something"], ["else"], {ASTs.RuleEnum.generates}),
                                                   ("bridge test;\nsomething generates one, two, three(val);", ["something"], ["one", "two", "three(val)"], {ASTs.RuleEnum.generates}),
                                                   ("bridge test\nsomething(value) generates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.generates}),
                                                   ("bridge test\nsomething(Variable) generates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.generates}),
                                                   ("bridge test\nsomething(_) generates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.generates}),
                                                   ):
            rules = result[0].rules
            self.assertAllIn((str(x.head) for x in rules), data[1])
            self.assertAllIn((str(y) for x in rules for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in rules), data[3])

    def test_inertial_rules(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\nsomething initiates else;", ["something"], ["else"], {ASTs.RuleEnum.initiates}),
                                                   ("bridge test;\nsomething initiates one, two, three(Var);", ["something"], ["one", "two", "three(Var)"], {ASTs.RuleEnum.initiates}),
                                                   ("bridge test\nsomething(value) initiates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.initiates}),
                                                   ("bridge test\nsomething(Variable) initiates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.initiates}),
                                                   ("bridge test\nsomething(_) initiates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.initiates}),

                                                   ("bridge test;\nsomething terminates else;", ["something"], ["else"], {ASTs.RuleEnum.terminates}),
                                                   ("bridge test;\nsomething terminates one, two, three(Var);", ["something"], ["one", "two", "three(Var)"], {ASTs.RuleEnum.terminates}),
                                                   ("bridge test\nsomething(value) terminates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.terminates}),
                                                   ("bridge test\nsomething(Variable) terminates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.terminates}),
                                                   ("bridge test\nsomething(_) terminates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.terminates}),
                                                   ):
            rules = result[0].rules
            self.assertAllIn((str(x.head) for x in rules), data[1])
            self.assertAllIn((str(y) for x in rules for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in rules), data[3])




    def test_transient_rules(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test.\nsomething when else.", ["something"], ["else"], {ASTs.RuleEnum.transient}),
                                                   ("bridge test.\nblah when bloo.", ["blah"], ["bloo"], {ASTs.RuleEnum.transient}),

                                                   ("bridge test.\nsomething when else.", ["something"], ["else"], {ASTs.RuleEnum.transient}),
                                                   ("bridge test.\nsomething(value) when else(other).", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.transient}),
                                                   ("bridge test.\nsomething(Variable) when else(Variable).", ["something(Variable)"], ["else(Variable)"], {ASTs.RuleEnum.transient}),
                                                   ("bridge test.\nsomething(Variable, SecondVar) when else(Variable, SecondVar).", ["something(Variable,SecondVar)"], ["else(Variable,SecondVar)"], {ASTs.RuleEnum.transient}),
                                                   ("bridge test.\nsomething(_) when else(_).", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.transient}),
                                                   ):
            transients = result[0].rules
            # all rules should have one body result:
            self.assertTrue(all(1 == len(x.body) for x in transients))
            self.assertTrue(all(x.head is None for x in transients))
            # Check the result of the rule:
            self.assertAllIn((str(y) for x in transients for y in x.body), data[1])
            # Check the conditions of the rule:
            self.assertAllIn((str(y.head) for x in transients for y in x.conditions), data[2])
            self.assertAllIn((x.annotation for x in transients), data[3])


    def test_initially(self):
        for result, data in self.yieldParseResults(b_dsl.top_bridge,
                                                   ("bridge test;\ninitially something;", ["something"]),
                                                   ("bridge test;\ninitially something(value);", ["something(value)"]),
                                                   ("bridge test;\ninitially something(Variable,SecondVar);", ["something(Variable,SecondVar)"]),
                                                   ("bridge test;\ninitially something(_,SecondVar);", ["something(_,SecondVar)"]),
                                                   ):
            initial = result[0].initial
            self.assertAllIn((str(y) for x in initial for y in x.body), data[1])


    @unittest.skip("TODO")
    def test_condition_parsing(self):
        pass

    def test_simple_full(self):
        self.assertFilesParse(b_dsl.top_bridge,
                              "test_bridge.iab",
                              loc=data_path)


##-- ifmain
if __name__ == '__main__':
    unittest.main()

##-- end ifmain
