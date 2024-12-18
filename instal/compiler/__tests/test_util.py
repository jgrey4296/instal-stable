#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from instal.compiler.util import CompileUtil
from instal.interfaces import ast as ASTs
from instal.parser.v2.parser import InstalPyParser


class TestCompilerUtils:

    def test_basic_term_recursive(self):
        term   = ASTs.TermAST("test")
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "test")

    def test_basic_term(self):
        term   = ASTs.TermAST("test")
        result = CompileUtil.compile_term(term)
        assert(result ==  "test")

    def test_term_with_params_recursive(self):
        term = ASTs.TermAST("test", params=[ASTs.TermAST("first"),
                                            ASTs.TermAST("second")])
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "test(first, second)")

    def test_term_with_params(self):
        term = ASTs.TermAST("test", params=[ASTs.TermAST("first"),
                                            ASTs.TermAST("second")])
        result = CompileUtil.compile_term(term)
        assert(result ==  "test(first, second)")

    def test_deontic_alt(self):
        term = ASTs.TermAST("permitted", [ASTs.TermAST("anAction", [ASTs.TermAST("X")])])
        result = CompileUtil.compile_term(term)
        assert(result ==  "deontic(permitted, anAction(X))")

    def test_nested_term_with_params(self):
        term = ASTs.TermAST("test", params=[ASTs.TermAST("something", [ASTs.TermAST("first")]),
                                            ASTs.TermAST("second")])
        result = CompileUtil.compile_term(term)
        assert(result ==  "test(something(first), second)")

    def test_term_with_params_and_underscore_recurisve(self):
        term = ASTs.TermAST("test_term", params=[ASTs.TermAST("first_a"),
                                                 ASTs.TermAST("second_b")])
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "test_term(first_a, second_b)")


    def test_deontic_term_translation_recursive(self):
        term = ASTs.TermAST("power", params=[ASTs.TermAST("something")])
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "deontic(power, something)")

    def test_deontic_term_translation(self):
        term = ASTs.TermAST("power", params=[ASTs.TermAST("something")])
        result = CompileUtil.compile_term(term)
        assert(result ==  "deontic(power, something)")

    def test_nested_deontic_term_translation_recursive(self):
        term = ASTs.TermAST("wrapper", [ASTs.TermAST("power", params=[ASTs.TermAST("something")])])
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "wrapper(deontic(power, something))")

    def test_nested_deontic_term_translation(self):
        term = ASTs.TermAST("wrapper", [ASTs.TermAST("power", params=[ASTs.TermAST("something")])])
        result = CompileUtil.compile_term(term)
        assert(result ==  "wrapper(deontic(power, something))")

    def test_bridge_deontic_term_translation_recursive(self):
        term = ASTs.TermAST("initPower", params=[ASTs.TermAST("source"),
                                                 ASTs.TermAST("action"),
                                                 ASTs.TermAST("sink")])
        result = CompileUtil.compile_term_recursive(term)
        assert(result ==  "deontic(initPower, ev(source, action, sink))")

    def test_bridge_deontic_term_translation(self):
        term = ASTs.TermAST("initPower", params=[ASTs.TermAST("source"),
                                                 ASTs.TermAST("action"),
                                                 ASTs.TermAST("sink")])
        result = CompileUtil.compile_term(term)
        assert(result ==  "deontic(initPower, ev(source, action, sink))")

    def test_type_wrapping_no_types(self):
        result = CompileUtil.wrap_types([], ASTs.TermAST("blah"))
        assert(result ==  {"true"})

    def test_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("has",
                            [ASTs.TermAST("Person", is_var=True),
                             ASTs.TermAST("Book", is_var=True)])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        assert(result ==  {"book(Book)","person(Person)", "true"})


    def test_nested_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("has",
                            [ASTs.TermAST("patron",
                                          [ASTs.TermAST("Person", is_var=True)]),
                             ASTs.TermAST("catalog",
                                          [ASTs.TermAST("Book", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        assert(result ==  {"book(Book)", "person(Person)", "true"})

    def test_multiple_same_type_wrapping(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book2", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        assert(result ==  {"book(Book1)", "book(Book2)", "true"})

    def test_multiple_same_type_wrapping_unique(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book1", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types, term)

        assert(result ==  {"book(Book1)", "true"})

    def test_multiple_same_type_wrapping_underscore(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        term = ASTs.TermAST("similarTo",
                            [ASTs.TermAST("fantasy",
                                          [ASTs.TermAST("Book_1", is_var=True)]),
                             ASTs.TermAST("romance",
                                          [ASTs.TermAST("Book_2", is_var=True)])])

        result = CompileUtil.wrap_types(inst.types,
                                        term)

        assert(result ==  {"book(Book_1)", "book(Book_2)", "true"})


    def test_empty_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        result    = CompileUtil.compile_conditions(inst, [])
        assert(result ==  {"true"})

    def test_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"))

        result    = CompileUtil.compile_conditions(inst, [condition])

        assert(result ==  {"holdsat(the_world, simple, I)", "true"})

    def test_comparison_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"),
                                      operator="<",
                                      rhs=ASTs.TermAST("the_universe"))

        result    = CompileUtil.compile_conditions(inst, [condition])

        assert(result ==  {"the_world<the_universe", "true"})

    def test_comparison_compilation_with_types(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world",
                                                   [ASTs.TermAST("Person", is_var=True)]),
                                      operator="<",
                                      rhs=ASTs.TermAST("the_universe",
                                                       [ASTs.TermAST("Person_2", is_var=True)]))

        result    = CompileUtil.compile_conditions(inst, [condition])

        assert(result ==  {"person(Person)",
                                  "person(Person_2)",
                                  "the_world(Person)<the_universe(Person_2)",
                                  "true"})

    def test_multiple_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"))
        condition2 = ASTs.ConditionAST(ASTs.TermAST("the_stars"))

        result    = CompileUtil.compile_conditions(inst, [condition, condition2])

        assert(result == {"holdsat(the_stars, simple, I)", "holdsat(the_world, simple, I)", "true"})

    def test_negated_condition_compilation(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world"),
                                      negated=True)

        result    = CompileUtil.compile_conditions(inst, [condition])

        assert(result ==  {"not holdsat(the_world, simple, I)", "true"})

    def test_condition_with_types(self):
        inst = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))

        condition = ASTs.ConditionAST(ASTs.TermAST("the_world",
                                                   [ASTs.TermAST("Person",
                                                                 is_var=True),
                                                    ASTs.TermAST("Person_2",
                                                                 is_var=True)]))

        result    = CompileUtil.compile_conditions(inst, [condition])

        assert(result ==  {"holdsat(the_world(Person, Person_2), simple, I)",
                                  "person(Person)",
                                  "person(Person_2)",
                                  "true"})



