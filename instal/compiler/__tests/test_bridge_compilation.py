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
from instal.parser.pyparse_institution import InstalPyParser
from insta.compiler.bridge_compiler import InstalBridgeCompiler
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
        inst     = ASTs.InstalBridgeDefAST(ASTs.TermAST("simple"))

        result = compiler.compile(inst)
        self.assertIsInstance(result, str)
        expected = [
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%% Compiled Institution",
            "%% simple",
            "%% From    : None",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "",
            "% Rules for Institution simple %",
            "inst(simple).",
            "ifluent(live(simple), simple).",
            "fluent(live(simple), simple).",
            "",
            ":- not _preludeLoaded.",
            "",
            " %%",
            " %-------------------------------",
            " % Part 1: Initial Setup and types",
            " % ",
            " %-------------------------------",
            " %",
            "",
            "%% null event for unknown events",
            "% Event: null (type: ex)",
            "event(null).",
            "event(viol(null)).",
            "",
            "evtype(null, simple, ex).",
            "evtype(viol(null), simple, viol).",
            "",
            "evinst(null, simple).",
            "evinst(viol(null), simple).",
            "",
            "ifluent(pow(null), simple).",
            "ifluent(perm(null), simple).",
            "fluent(pow(null), simple).",
            "fluent(perm(null), simple).",
            "",
            "% no creation event",
            "holdsat(live(simple), simple, I) :- start(I), inst(simple).",
            "holdsat(perm(null), simple, I)    :- start(I), inst(simple).",
            "holdsat(pow(null), simple, I)     :- start(I), inst(simple).",
            "",
            " %%",
            " %-------------------------------",
            " % Part 2: Generation and Consequence",
            " % ",
            " %-------------------------------",
            " %",
            "",
            " %%",
            " %-------------------------------",
            " % Part 3: Initial Situation Specification",
            " % ",
            " %-------------------------------",
            " %",
            "",
            "",
            " %%",
            " %-------------------------------",
            " % Type Grounding and declaration",
            " % ",
            " %-------------------------------",
            " %",
            "",
            "%% End of simple",
            ]
        self.assertEqual(len(result.split("\n")), len(expected))
        for x,y in zip(result.split("\n"), expected):
            self.assertEqual(x,y)



if __name__ == '__main__':
    unittest.main()
