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
import instal.parser.parse_funcs as dsl
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- data
data_path = files("instal.parser.__tests.__data")
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

    def test_sources(self):
        for result, data in self.yieldParseResults(dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsource bloo;\nsource other;", ["bloo", "other"]),
                                                   ):
            sources = (x.value for x in result[0].sources)
            self.assertAllIn(sources, data[1])

    def test_sinks(self):
        for result, data in self.yieldParseResults(dsl.top_bridge,
                                                   ("bridge test;\ntype Test;\nsource bloo;\nsource other;", ["bloo", "other"]),
                                                   ):
            sinks = (x.value for x in result[0].sinks)
            self.assertAllIn(sinks, data[1])

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
                                                   ("institution test;\nnoninertial fluent testFluent;\nnoninertial fluent otherFluent;", ["testFluent", "otherFluent"], {ASTs.FluentEnum.noninertial}),
                                                   ("institution test;\nobligation fluent obFluent(obligation, deadline, violation);", ["obFluent"], {ASTs.FluentEnum.obligation}),
                                                   ("institution test;\ncross fluent blah;", ["blah"], {ASTs.FluentEnum.cross}),
                                                   ):
            fluents = result[0].fluents
            self.assertAllIn((x.head.value for x in fluents), data[1])
            self.assertAllIn((x.annotation for x in fluents), data[2])

    def test_generation(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething initiates else;", ["something"], ["else"], {ASTs.RelationalEnum.initiates}),
                                                   ("institution test;\nsomething generates else;", ["something"], ["else"], {ASTs.RelationalEnum.generates}),
                                                   ):
            relations = result[0].relations
            self.assertAllIn((x.head.value for x in relations), data[1])
            self.assertAllIn((y.value for x in relations for y in x.body), data[2])
            self.assertAllIn((x.annotation for x in relations), data[3])

    def test_nifs(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ("institution test;\nsomething when else;", ["something"], ["else"]),
                                                   ):
            nifs = result[0].nif_rules
            self.assertAllIn((x.head.value for x in nifs), data[1])
            self.assertAllIn((y.value for x in nifs for y in x.body), data[2])


    def test_initially(self):
        for result, data in self.yieldParseResults(dsl.top_institution,
                                                   ("institution test;\ninitially something;", ["something"]),
                                                   ):
            initial = result[0].initial
            self.assertAllIn((y.value for x in initial for y in x.body), data[1])


    @unittest.skip("TODO")
    def test_condition_parsing(self):
        pass

    def test_simple_full(self):
        self.assertFilesParse(dsl.top_institution,
                              "test_inst.ial",
                              "test_inst2.ial",
                              loc=data_path)


if __name__ == '__main__':
    unittest.main()
