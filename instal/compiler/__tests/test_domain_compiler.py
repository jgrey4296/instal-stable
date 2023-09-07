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
from instal.parser.v2.parser import InstalPyParser
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.interfaces import ast as ASTs

class TestDomainCompiler:
    def test_one_type_domain(self):
        """ initially/iaf -> .lp """
        compiler = InstalDomainCompiler()
        data     = []
        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Person"),
                                            [ASTs.TermAST("bill"),
                                             ASTs.TermAST("jill")]))

        result = compiler.compile(data)
        assert(result == str)
        expected = [
            "%%",
            "%-------------------------------",
            "% Domain Specification",
            "% n/a",
            "%-------------------------------",
            "%%",
            "",
            "#program base.",
            "",
            "definedType(person).",
            "person(bill).",
            "person(jill).",
            ]
        assert(len(result.split("\n")) == len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)

    def test_two_type_domain(self):
        """ initially/iaf -> .lp """
        compiler = InstalDomainCompiler()
        data     = []
        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Person"),
                                            [ASTs.TermAST("bill"),
                                             ASTs.TermAST("jill")]))

        data.append(ASTs.DomainSpecAST(ASTs.TermAST("Book"),
                                            [ASTs.TermAST("book1"),
                                             ASTs.TermAST("book2")]))

        result = compiler.compile(data)
        assert(isinstance(result, str))
        expected = [
            "%%",
            "%-------------------------------",
            "% Domain Specification",
            "% n/a",
            "%-------------------------------",
            "%%",
            "",
            "#program base.",
            "",
            "definedType(person).",
            "person(bill).",
            "person(jill).",
            "definedType(book).",
            "book(book1).",
            "book(book2).",
            ]
        assert(len(result.split("\n")) == len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)
