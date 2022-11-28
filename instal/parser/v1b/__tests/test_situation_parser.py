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

import instal.parser.v1b.parse_funcs as dsl
import instal.interfaces.ast as ASTs
from instal.interfaces.parser import InstalParserTestCase
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestSituationParser(InstalParserTestCase):

    def test_simple_situation(self):
        self.assertParseResultsIsInstance(dsl.top_fact,
                                          ("initially(basicfact, greeting)", ASTs.InitiallyAST),
                                          ("initially(basic(blah), greeting)", ASTs.InitiallyAST),
                                          )

    def test_situation_contents(self):
        for result, data in self.yieldParseResults(dsl.top_fact,
                                                   ("initially(basicfact, greeting)", "greeting", 1),
                                                   ("initially(basic(blah), greeting)\ninitially(other, greeting)", "greeting", 2),
                                                   ("""initially(basic(blah), greeting)
                                                   initially(other, greeting)
                                                   initially(another, greeting)""", "greeting", 3),
                                                   ("initially(basic(blah), other)",  "other",    1, "basic", "blah"),
                                                   ):
            match data:
                case text, inst, length:
                    self.assertEqual(len(result), length)
                    self.assertEqual(result[0].inst.value, inst)
                case text, inst, length, fact, param:
                    self.assertEqual(len(result), length)
                    self.assertEqual(result[0].inst.value, inst)
                    self.assertEqual(result[0].body[0].value, fact)
                    self.assertEqual(result[0].body[0].params[0].value, param)


##-- ifmain
if __name__ == '__main__':
    unittest.main()

##-- end ifmain
