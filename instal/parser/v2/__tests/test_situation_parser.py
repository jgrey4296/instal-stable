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
import instal.parser.v2.parse_funcs as dsl
import instal.interfaces.ast as ASTs
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

class TestSituationParser(InstalParserTestCase):

    def test_simple_situation(self):
        self.assertParseResultsIsInstance(dsl.top_fact,
                                          ("initially basicfact in greeting", ASTs.InitiallyAST),
                                          ("initially basic(blah) in greeting", ASTs.InitiallyAST),
                                          )

    def test_situation_contents(self):
        for result, data in self.yieldParseResults(dsl.top_fact,
                                                   ("initially basicfact in greeting", "greeting", 1),
                                                   ("initially basic(blah) in greeting\ninitially other in greeting", "greeting", 2),
                                                   ("""initially basic(blah) in greeting
                                                   initially other in greeting
                                                   initially another in greeting""", "greeting", 3),
                                                   ("initially basic(blah) in other",  "other",    1, "basic", "blah"),
                                                   ):
            match data:
                case text, inst, length:
                    assert(len(result)          == length)
                    assert(result[0].inst.value == inst)
                case text, inst, length, fact, param:
                    assert(len(result)                       == length)
                    assert(result[0].inst.value              == inst)
                    assert(result[0].body[0].value           == fact)
                    assert(result[0].body[0].params[0].value == param, "testmsg")
