#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import unittest
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.compiler.util import CompileUtil
from instal.interfaces import ast as ASTs
from instal.parser.pyparse_institution import InstalPyParser

##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestCompilerUtils(unittest.TestCase):
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

    def test_basic_term(self):
        term   = ASTs.TermAST("test")
        result = CompileUtil.compile_term(term)
        self.assertEqual(result, "test")

    def test_term_with_params(self):
        term = ASTs.TermAST("test", params=[ASTs.TermAST("first"),
                                            ASTs.TermAST("second")])
        result = CompileUtil.compile_term(term)
        self.assertEqual(result, "test(first, second)")

    def test_term_with_params_and_underscore(self):
        term = ASTs.TermAST("test_term", params=[ASTs.TermAST("first_a"),
                                                 ASTs.TermAST("second_b")])
        result = CompileUtil.compile_term(term)
        self.assertEqual(result, "testterm(firsta, secondb)")


    def test_type_wrapping_no_types(self):
        result = CompileUtil.wrap_types([], ASTs.TermAST("blah"))
        self.assertEqual(result, {"true"})

    def test_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("has",
                            [ASTs.TermAST("Person", is_var=True),
                             ASTs.TermAST("Book", is_var=True)])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        self.assertEqual(result, {"book(Book)","person(Person)", "true"})


    def test_nested_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("has",
                            [ASTs.TermAST("patron",
                                          [ASTs.TermAST("Person", is_var=True)]),
                             ASTs.TermAST("catalog",
                                          [ASTs.TermAST("Book", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        self.assertEqual(result, {"book(Book)", "person(Person)", "true"})

    def test_multiple_same_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book2", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        self.assertEqual(result, {"book(Book1)", "book(Book2)", "true"})

    def test_multiple_same_type_wrapping_unique(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book1", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types, term)

        self.assertEqual(result, {"book(Book1)", "true"})

    def test_multiple_same_type_wrapping_underscore(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book_1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book_2", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        self.assertEqual(result, {"book(Book1)", "book(Book2)", "true"})


    def test_empty_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        result    = CompileUtil.compile_conditions(inst, [])
        self.assertEqual(result, {"true"})

    def test_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"))

        result    = CompileUtil.compile_conditions(inst, [condition])

        self.assertEqual(result, {"holdsat(theworld, simple, I)", "true"})

    def test_comparison_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"),
                                      operator="<",
                                      rhs=ASTs.TermAST("the_universe"))

        result    = CompileUtil.compile_conditions(inst, [condition])

        self.assertEqual(result, {"theworld<theuniverse", "true"})

    def test_comparison_compilation_with_types(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world",
                                                   [ASTs.TermAST("Person", is_var=True)]),
                                      operator="<",
                                      rhs=ASTs.TermAST("the_universe",
                                                       [ASTs.TermAST("Person_2", is_var=True)]))

        result    = CompileUtil.compile_conditions(inst, [condition])

        self.assertEqual(result, {"person(Person)",
                                  "person(Person2)",
                                  "theworld(Person)<theuniverse(Person2)",
                                  "true"})

    def test_multiple_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"))
        condition2 = ASTs.ConditionAST(ASTs.TermAST("the_stars"))

        result    = CompileUtil.compile_conditions(inst, [condition, condition2])

        self.assertEqual(result,
                         {"holdsat(thestars, simple, I)",
                          "holdsat(theworld, simple, I)",
                          "true"})

    def test_negated_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"),
                                      negated=True)

        result    = CompileUtil.compile_conditions(inst, [condition])

        self.assertEqual(result, {"not holdsat(theworld, simple, I)", "true"})

    def test_condition_with_types(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world",
                                                   [ASTs.TermAST("Person",
                                                                 is_var=True),
                                                    ASTs.TermAST("Person_2",
                                                                 is_var=True)]))

        result    = CompileUtil.compile_conditions(inst, [condition])

        self.assertEqual(result, {"holdsat(theworld(Person, Person2), simple, I)",
                                  "person(Person)",
                                  "person(Person2)",
                                  "true"})



if __name__ == '__main__':
    unittest.main()
