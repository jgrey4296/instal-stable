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
import instal.parser.v2.institution_parse_funcs as i_dsl
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
        self.assertParseResultsIsInstance(i_dsl.top_institution,
                                          ("institution simple;\ntype Test;", ASTs.InstitutionDefAST),
                                          )

    def test_simple_bridge(self):
        self.assertParseResultsIsInstance(i_dsl.top_bridge,
                                          ("bridge test;\ntype Test;\nsink blah;", ASTs.BridgeDefAST),
                                          )

    def test_sources(self):
        for result, data in self.yieldParseResults(i_dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsource bloo;\nsource other;", ["bloo", "other"]),
                                                   ):
            sources = (x.value for x in result[0].sources)
            self.assertAllIn(sources, data[1])

    def test_sinks(self):
        for result, data in self.yieldParseResults(i_dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsource bloo;\nsource other;", ["bloo", "other"]),
                                                   ):
            sinks = (x.value for x in result[0].sinks)
            self.assertAllIn(sinks, data[1])

    def test_types(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\ntype Test;\ntype Other;", ["Test", "Other"])
                                                   ):
            types = (x.head.value for x in result[0].types)
            self.assertAllIn(types, data[1])

    def test_events(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\nexogenous event blah;\nexogenous event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),
                                                   ("institution test;\nexo event blah;\nexo event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),
                                                   ("institution test;\nexternal event blah;\nexternal event other;", ["blah", "other"], {ASTs.EventEnum.exogenous}),

                                                   ("institution test;\ninstitutional event blah;\ninstitutional event other;\ninstitutional event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),
                                                   ("institution test;\ninst event blah;\ninst event other;\ninst event another;", ["blah", "other", "another"], {ASTs.EventEnum.institutional}),


                                                   ("institution test;\nviolation event blah;\nviolation event other;\nviolation event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ("institution test;\nviol event blah;\nviol event other;\nviol event another;", ["blah", "other", "another"], {ASTs.EventEnum.violation}),
                                                   ):
            events = result[0].events
            self.assertAllIn((x.head.value for x in events), data[1])
            self.assertAllIn((x.annotation for x in events), data[2])


    def test_fluents(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\nfluent testFluent;\nfluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.inertial}),

                                                   ("institution test;\ntransient fluent testFluent;\ntransient fluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.transient}),

                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation, oneshot);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation, multishot);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("institution test;\nobl fluent obFluent(obligation, deadline, violation, multishot);", ["obFluent"], {ASTs.FluentEnum.obligation}),

                                                   ("institution test;\ncross fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ("institution test;\nx fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ):

            fluents = result[0].fluents
            self.assertAllIn((x.head.value for x in fluents), data[1])
            self.assertAllIn((x.annotation for x in fluents), data[2])

    def test_generation_rules(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\nsomething generates else;", ["something"], ["else"], {ASTs.RuleEnum.generates}),
                                                   ("institution test;\nsomething generates one, two, three(val);", ["something"], ["one", "two", "three(val)"], {ASTs.RuleEnum.generates}),
                                                   ("institution test\nsomething(value) generates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.generates}),
                                                   ("institution test\nsomething(Variable) generates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.generates}),
                                                   ("institution test\nsomething(_) generates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.generates}),
                                                   ):
            rules = result[0].rules
            self.assertAllIn((str(x.head) for x in rules), data[1])
            self.assertAllIn((str(y) for x in rules for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in rules), data[3])

    def test_inertial_rules(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\nsomething initiates else;", ["something"], ["else"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test;\nsomething initiates one, two, three(Var);", ["something"], ["one", "two", "three(Var)"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test\nsomething(value) initiates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test\nsomething(Variable) initiates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.initiates}),
                                                   ("institution test\nsomething(_) initiates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.initiates}),

                                                   ("institution test;\nsomething terminates else;", ["something"], ["else"], {ASTs.RuleEnum.terminates}),
                                                   ("institution test;\nsomething terminates one, two, three(Var);", ["something"], ["one", "two", "three(Var)"], {ASTs.RuleEnum.terminates}),
                                                   ("institution test\nsomething(value) terminates else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.terminates}),
                                                   ("institution test\nsomething(Variable) terminates else(Other)", ["something(Variable)"], ["else(Other)"], {ASTs.RuleEnum.terminates}),
                                                   ("institution test\nsomething(_) terminates else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.terminates}),
                                                   ):
            rules = result[0].rules
            self.assertAllIn((str(x.head) for x in rules), data[1])
            self.assertAllIn((str(y) for x in rules for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in rules), data[3])




    def test_transient_rules(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\nsomething when else;", ["something"], ["else"], {ASTs.RuleEnum.transient}),
                                                   ("institution test;\nblah when bloo;", ["blah"], ["bloo"], {ASTs.RuleEnum.transient}),

                                                   ("institution test;\nsomething when else;", ["something"], ["else"], {ASTs.RuleEnum.transient}),
                                                   ("institution test\nsomething(value) when else(other)", ["something(value)"], ["else(other)"], {ASTs.RuleEnum.transient}),
                                                   ("institution test\nsomething(Variable) when else(Variable)", ["something(Variable)"], ["else(Variable)"], {ASTs.RuleEnum.transient}),
                                                   ("institution test\nsomething(Variable, SecondVar) when else(Variable, SecondVar)", ["something(Variable, SecondVar)"], ["else(Variable, SecondVar)"], {ASTs.RuleEnum.transient}),
                                                   ("institution test\nsomething(_) when else(_)", ["something(_)"], ["else(_)"], {ASTs.RuleEnum.transient}),
                                                   ):
            transients = result[0].rules
            self.assertAllIn((str(x.head) for x in transients), data[1])
            self.assertAllIn((str(y) for x in transients for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in transients), data[3])


    def test_initially(self):
        for result, data in self.yieldParseResults(i_dsl.top_institution,
                                                   ("institution test;\ninitially something;", ["something"]),
                                                   ("institution test;\ninitially something(value);", ["something(value)"]),
                                                   ("institution test;\ninitially something(Variable, SecondVar);", ["something(Variable, SecondVar)"]),
                                                   ("institution test;\ninitially something(_, SecondVar);", ["something(_, SecondVar)"]),
                                                   ):
            initial = result[0].initial
            self.assertAllIn((str(y) for x in initial for y in x.body), data[1])


    @unittest.skip("TODO")
    def test_condition_parsing(self):
        pass

    def test_simple_full(self):
        self.assertFilesParse(i_dsl.top_institution,
                              "test_inst.ial",
                              "test_inst2.ial",
                              "test_inst3.ial",
                              loc=data_path)


if __name__ == '__main__':
    unittest.main()
