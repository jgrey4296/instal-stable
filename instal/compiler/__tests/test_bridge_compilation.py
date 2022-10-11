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
from instal.parser.v2.parser import InstalPyParser
from instal.compiler.bridge_compiler import InstalBridgeCompiler
from instal.interfaces import ast as ASTs
from unittest import mock
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestBridgeCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_simple_bridge(self):
        compiler = InstalBridgeCompiler()
        inst     = ASTs.BridgeDefAST(ASTs.TermAST("simple"))
        inst.sources.append(ASTs.TermAST("sourceTest"))
        inst.sinks.append(ASTs.TermAST("sinkTest"))

        result = compiler.compile([inst])
        self.assertIsInstance(result, str)
        expected = [
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%% Compiled Bridge",
            "%% simple",
            "%% From : ",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "#program base.",
            "",
            "% bridge/3 (in standard prelude) is built from these:",
            "institution(simple).",
            "source(sourceTest, simple).",
            "sink(sinkTest, simple).",
            "",
            ":- not _preludeLoaded.",
            "",
            "%%",
            "%-------------------------------",
            "% Part 1: Events and Fluents",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "%%",
            "%-------------------------------",
            "% Part 2: Generation and Consequence",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "%%",
            "%-------------------------------",
            "% Part 3: Initial Situation Specification",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "#program base.",
            "",
            "%%",
            "%-------------------------------",
            "% Type Grounding and declaration",
            "% ",
            "%-------------------------------",
            "%%",
            "",
            "%% End of simple",
            ]
        # self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)




    def test_cross_fluents(self):
        compiler = InstalBridgeCompiler()
        inst     = ASTs.BridgeDefAST(ASTs.TermAST("simple"))
        inst.sources.append(ASTs.TermAST("sourceTest"))
        inst.sinks.append(ASTs.TermAST("sinkTest"))

        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("ipow",
                                                        [ASTs.TermAST("first"),
                                                         ASTs.TermAST("second"),
                                                         ASTs.TermAST("third")]),
                                           ASTs.FluentEnum.cross))


        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "inertialFluent(ipow(first, second, third), simple) :- bridge(simple, first, third), true.",
            ""
            ]
        # self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

    def test_cross_generation(self):
        compiler = InstalBridgeCompiler()
        inst     = ASTs.BridgeDefAST(ASTs.TermAST("simple"))
        inst.sources.append(ASTs.TermAST("sourceTest"))
        inst.sinks.append(ASTs.TermAST("sinkTest"))

        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("test"),
                                                 [ASTs.TermAST("testResult")],
                                                 annotation=ASTs.RuleEnum.xgenerates))


        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of test of sourceTest xgenerates testResult of sinkTest if [condition] in",
            "occurred(testResult, sinkTest, I) :- instant(I),",
            "bridge(simple,  sourceTest,  sinkTest)",
            "holdsat(gpow(sourceTest, testResult, sinkTest), simple, I),",
            "occurred(test, sourceTest, I),",
            "true.",
            ""
            ]
        # self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x.strip(),y.strip())

    def test_cross_initiates(self):
        compiler = InstalBridgeCompiler()
        inst     = ASTs.BridgeDefAST(ASTs.TermAST("simple"))
        inst.sources.append(ASTs.TermAST("sourceTest"))
        inst.sinks.append(ASTs.TermAST("sinkTest"))

        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("test"),
                                               [ASTs.TermAST("testResult")],
                                               annotation=ASTs.RuleEnum.xinitiates))


        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of test of sourceTest xinitiates testResult of sinkTest if [condition]",
            "xinitiated(sourceTest, testResult, sinkTest, I) :- instant(I),",
            "bridge(simple, sourceTest, sinkTest),",
            "holdsat(ipow(sourceTest, testResult, sinkTest), simple, I),",
            "holdsat(live(simple), simple, I),",
            "occurred(test, sourceTest, I),",
            "true.",
            ""
            ]
        # self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x.strip(),y.strip())


    def test_cross_terminates(self):
        compiler = InstalBridgeCompiler()
        inst     = ASTs.BridgeDefAST(ASTs.TermAST("simple"))
        inst.sources.append(ASTs.TermAST("sourceTest"))
        inst.sinks.append(ASTs.TermAST("sinkTest"))

        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("test"),
                                               [ASTs.TermAST("testResult")],
                                               annotation=ASTs.RuleEnum.xterminates))


        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of test of sourceTest xterminates testResult of sinkTest if [condition]",
            "xterminated(sourceTest, testResult, sinkTest, I) :- instant(I),",
            "bridge(simple, sourceTest, sinkTest),",
            "holdsat(tpow(sourceTest, testResult, sinkTest), simple, I),",
            "holdsat(live(simple), simple, I),",
            "occurred(test, sourceTest, I),",
            "true.",
            ""
            ]
        # self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x.strip(),y.strip())

if __name__ == '__main__':
    unittest.main()
