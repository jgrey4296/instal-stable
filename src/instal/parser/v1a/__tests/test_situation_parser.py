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
##-- end imports


class TestSituationParser(InstalParserTestCase):

    def test_simple_situation(self):
        self.assertParseResultsIsInstance(dsl.top_fact,
                                          ("initially(greeting, basicfact)", ASTs.InitiallyAST),
                                          ("initially(greeting, basic(blah))", ASTs.InitiallyAST),
                                          )

    def test_situation_contents(self):
        for result, data in self.yieldParseResults(dsl.top_fact,
                                                   ("initially(greeting, basicfact)", "greeting", 1),
                                                   ("initially(greeting, basic(blah))\ninitially(greeting, other)", "greeting", 2),
                                                   ("""initially(greeting, basic(blah))
                                                   initially(greeting,other)
                                                   initially(greeting, another)""", "greeting", 3),
                                                   ("initially(other, basic(blah))",  "other",    1, "basic", "blah"),
                                                   ):
            match data:
                case text, inst, length:
                    assert(len(result) == length)
                    assert(result[0].inst.value == inst)
                case text, inst, length, fact, param:
                    assert(len(result)                       == length)
                    assert(result[0].inst.value              == inst)
                    assert(result[0].body[0].value           == fact)
                    assert(result[0].body[0].params[0].value == param)
