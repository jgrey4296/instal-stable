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

from instal.parser.pyparse_institution import InstalPyParser
import instal.interfaces.ast as ASTs
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestInstitutionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

        cls.dsl = InstalPyParser()


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)


    def test_simple_institution(self):
        result = self.dsl.parse_institution("institution simple;\ntype Test;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertEqual(result.head.value, "simple")

    def test_bridge_name(self):
        result = self.dsl.parse_bridge("bridge test;\ntype Test;\nsink blah;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertEqual(result.head.value, "test")

    def test_sources(self):
        result = self.dsl.parse_bridge("bridge test;\ntype Test;\nsource bloo;\nsource other;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.TermAST) for x in result.sources))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.sources[0].value, "bloo")
        self.assertEqual(result.sources[1].value, "other")

    def test_sinks(self):
        result = self.dsl.parse_bridge("bridge test;\ntype Test;\nsink blah;\nsink bloo;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.TermAST) for x in result.sinks))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.sinks[0].value, "blah")
        self.assertEqual(result.sinks[1].value, "bloo")

    def test_types(self):
        result = self.dsl.parse_institution("institution test;\ntype Test;\ntype Other;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.TypeAST) for x in result.types))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.types[0].head.value, "Test")
        self.assertEqual(result.types[1].head.value, "Other")

    def test_events(self):
        result = self.dsl.parse_institution("institution test;\nexogenous event blah;\nexogenous event other;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.EventAST) for x in result.events))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.events[0].head.value, "blah")
        self.assertEqual(result.events[1].head.value, "other")

    def test_event_types(self):
        result = self.dsl.parse_institution("institution test;\nexogenous event blah;\ninst event other;\nviolation event another;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.events[0].head.value, "blah")
        self.assertEqual(result.events[1].head.value, "other")
        self.assertEqual(result.events[2].head.value, "another")

        self.assertEqual(result.events[0].annotation, ASTs.EventEnum.exogenous)
        self.assertEqual(result.events[1].annotation, ASTs.EventEnum.institutional)
        self.assertEqual(result.events[2].annotation, ASTs.EventEnum.violation)

    def test_fluents(self):
        result = self.dsl.parse_institution("institution test;\nfluent testFluent;\nfluent otherFluent;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.FluentAST) for x in result.fluents))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.fluents[0].head.value, "testFluent")
        self.assertEqual(result.fluents[1].head.value, "otherFluent")

    def test_fluent_types(self):
        result = self.dsl.parse_institution("institution test;\nfluent testFluent;\nnoninertial fluent otherFluent;\nobligation fluent obFluent(obligation, deadline, violation);\ncross fluent blah;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.FluentAST) for x in result.fluents))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.fluents[0].head.value, "testFluent")
        self.assertEqual(result.fluents[1].head.value, "otherFluent")
        self.assertEqual(result.fluents[2].head.value, "obFluent")
        self.assertEqual(result.fluents[3].head.value, "blah")

        self.assertEqual(result.fluents[0].annotation, None)
        self.assertEqual(result.fluents[1].annotation, ASTs.FluentEnum.noninertial)
        self.assertEqual(result.fluents[2].annotation, ASTs.FluentEnum.obligation)
        self.assertEqual(result.fluents[3].annotation, ASTs.FluentEnum.cross)

    def test_generation(self):
        result = self.dsl.parse_institution("institution test;\nsomething initiates else;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.RelationalAST) for x in result.relations))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.relations[0].head.value, "something")
        self.assertEqual(result.relations[0].body[0].value, "else")
        self.assertEqual(result.relations[0].annotation, ASTs.RelationalEnum.initiates)

    def test_consequence(self):
        result = self.dsl.parse_institution("institution test;\nsomething generates else;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.RelationalAST) for x in result.relations))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.relations[0].head.value, "something")
        self.assertEqual(result.relations[0].body[0].value, "else")
        self.assertEqual(result.relations[0].annotation, ASTs.RelationalEnum.generates)

    def test_nifs(self):
        result = self.dsl.parse_institution("institution test;\nsomething when else;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.NifRuleAST) for x in result.nif_rules))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.nif_rules[0].head.value, "something")
        self.assertEqual(result.nif_rules[0].body[0].value, "else")

    def test_initially(self):
        result = self.dsl.parse_institution("institution test;\ninitially something;")
        self.assertIsInstance(result, ASTs.InstitutionDefAST)
        self.assertTrue(all(isinstance(x, ASTs.InitiallyAST) for x in result.initial))
        self.assertEqual(result.head.value, "test")
        self.assertEqual(result.initial[0].body[0].value, "something")


    def test_condition_parsing(self):
        pass



if __name__ == '__main__':
    unittest.main()
