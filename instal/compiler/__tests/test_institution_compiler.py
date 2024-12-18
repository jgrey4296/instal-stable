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
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.interfaces import ast as ASTs

class TestInstitutionCompiler:

    def test_simple_institution(self):
        compiler = InstalInstitutionCompiler()
        inst     = [ASTs.InstitutionDefAST(ASTs.TermAST("simple"))]

        result = compiler.compile(inst)
        assert(isinstance(result, str))
        expected = [
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%% Compiled Institution",
            "%% simple",
            "%% From    : n/a",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "#program base.",
            "",
            "% Basic Fact for Institution simple %",
            "institution(simple).",
            "",
            ":- not _preludeLoaded.",
            "",
            "%%",
            "%-------------------------------",
            "% Part 1: Initial Setup and types",
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
        assert(len(result.split("\n")) ==  len(expected))
        for x,y in zip(result.split("\n"), expected):
            assert(x == y)

    def test_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.exogenous))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: EventEnum.exogenous)",
            "eventType(greet, simple, ex) :- true.",
            "",
            ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_multiple_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.exogenous))

        inst.events.append(ASTs.EventAST(ASTs.TermAST("accuse"),
                                         ASTs.EventEnum.exogenous))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: EventEnum.exogenous)",
            "eventType(greet, simple, ex) :- true.",
            "",
            "% Event: accuse (type: EventEnum.exogenous)",
            "eventType(accuse, simple, ex) :- true.",
            "",
            ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_inst_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.institutional))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: EventEnum.institutional)",
            "eventType(greet, simple, inst) :- true.",
            "",
            ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_violation_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.violation))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: EventEnum.violation)",
            "eventType(greet, simple, viol) :- true.",
            "",
            ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_events_with_types_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet",
                                                      [ASTs.TermAST("Person_1",
                                                                    is_var=True),
                                                       ASTs.TermAST("Person_2",
                                                                    is_var=True)]),
                                         ASTs.EventEnum.violation))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet(Person_1, Person_2) (type: EventEnum.violation)",
            "eventType(greet(Person_1, Person_2), simple, viol) :- person(Person_1), person(Person_2), true.",
            "",
            ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_fluent_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive"),
                                           ASTs.FluentEnum.inertial))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% inertial fluent: alive %",
            "inertialFluent(alive, simple) :- true.",
            ""
        ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_fluent_with_types_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive",
                                                        [ASTs.TermAST("Person",
                                                                      is_var=True)]),
                                           ASTs.FluentEnum.inertial))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% inertial fluent: alive(Person) %",
            "inertialFluent(alive(Person), simple) :- person(Person), true.",
            ""
        ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_fluent_obligation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("avenge",
                                                        [ASTs.TermAST("requirementTest"),
                                                         ASTs.TermAST("deadlineTest"),
                                                         ASTs.TermAST("violTest"),
                                                         ]),
                                           ASTs.FluentEnum.achievement_obligation))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% obligation fluent: avenge(requirementTest, deadlineTest, violTest) %",
            "obligationFluent(obligation(avenge, requirementTest, deadlineTest, violTest), simple) :- institution(simple),",
            "eventType(requirementTest, simple, inst),",
            "eventType(deadlineTest, simple, inst),",
            "eventType(violTest, simple, inst),",
            "true.",
            "",
            "obligationType(avenge, achievement, simple).",
            "",
            "% as function heads can't be variables,",
            "% convert name(...) to obligation(name ...) for internal use",
            "inertialFluent(avenge(requirementTest, deadlineTest, violTest), simple) :- institution(simple).",
            "",
            "% but make sure they sync:",
            "inertialFluentChange(obligation(avenge, R, D, V), simple, I, C) :- inertialFluentChange(avenge(R, D, V), simple, I, C).",
            "inertialFluentChange(avenge(R, D, V), simple, I, C)             :- inertialFluentChange(obligation(avenge, R, D, V), simple, I, C).",
            "",
        ]
        for x,y in zip(result, expected):
            assert(x.strip() ==  y)

        assert(len(result) ==  len(expected))

    def test_fluent_non_inertial(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive"),
                                           ASTs.FluentEnum.transient))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% noninertial/transient fluent: alive %",
            "transientFluent(alive, simple) :- true.",
            ""
        ]
        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x == y)

    def test_generation_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("alive"),
                                                 [ASTs.TermAST("breathing")],
                                                 annotation=ASTs.RuleEnum.generates,
                                                 ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive generates breathing if [condition] (in )",
            "%% Ex Event generates Inst Event:",
            "occurred(breathing, simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive, simple, ex),",
            "eventType(breathing, simple, inst),",
            "holdsat(deontic(power, breathing), simple, I),",
            "observed(alive, I),",
            "true.",
            "",
            "%% Inst Event Generates Inst Event",
            "occurred(breathing, simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive, simple, inst),",
            "eventType(breathing, simple, inst),",
            "holdsat(deontic(power, breathing), simple, I),",
            "occurred(alive, simple, I),",
            "true.",
            "",
            "%% Unempowered event generation",
            "occurred(_unempoweredEvent(breathing), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive, simple, ex),",
            "eventType(breathing, simple, inst),",
            "not holdsat(deontic(power, breathing), simple, I),",
            "observed(alive, I),",
            "true.",
            "",
            "occurred(_unempoweredEvent(breathing), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive, simple, inst),",
            "eventType(breathing, simple, inst),",
            "not holdsat(deontic(power, breathing), simple, I),",
            "occurred(alive, simple, I),",
            "true.",
            "",
            "%% Unpermitted event generation",
            "occurred(_unpermittedEvent(breathing), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(breathing, simple, inst),",
            "holdsat(deontic(power, breathing), simple, I),",
            "not holdsat(deontic(permitted, breathing), simple, I),",
            "occurred(breathing, simple, I),",
            "true.",
            "",
        ]

        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x.strip() == y)

    def test_generation_with_types(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                                 [ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)])],
                                                 annotation=ASTs.RuleEnum.generates,
                                                 ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive(Person) generates breathing(Person) if [condition] (in )",
            "%% Ex Event generates Inst Event:",
            "occurred(breathing(Person), simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, ex),",
            "eventType(breathing(Person), simple, inst),",
            "holdsat(deontic(power, breathing(Person)), simple, I),",
            "observed(alive(Person), I),",
            "person(Person), true.",
            "",
            "%% Inst Event Generates Inst Event",
            "occurred(breathing(Person), simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, inst),",
            "eventType(breathing(Person), simple, inst),",
            "holdsat(deontic(power, breathing(Person)), simple, I),",
            "occurred(alive(Person), simple, I),",
            "person(Person), true.",
            "",
            "%% Unempowered event generation",
            "occurred(_unempoweredEvent(breathing(Person)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, ex),",
            "eventType(breathing(Person), simple, inst),",
            "not holdsat(deontic(power, breathing(Person)), simple, I),",
            "observed(alive(Person), I),",
            "person(Person), true.",
            "",
            "occurred(_unempoweredEvent(breathing(Person)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, inst),",
            "eventType(breathing(Person), simple, inst),",
            "not holdsat(deontic(power, breathing(Person)), simple, I),",
            "occurred(alive(Person), simple, I),",
            "person(Person), true.",
            "",
            "%% Unpermitted event generation",
            "occurred(_unpermittedEvent(breathing(Person)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(breathing(Person), simple, inst),",
            "holdsat(deontic(power, breathing(Person)), simple, I),",
            "not holdsat(deontic(permitted, breathing(Person)), simple, I),",
            "occurred(breathing(Person), simple, I),",
            "person(Person), true.",
            "",
        ]

        assert(len(result) ==  len(expected))
        for x,y in zip(result, expected):
            assert(x.strip() == y)

    def test_generation_with_condition(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                                 [ASTs.TermAST("breathing", [ASTs.TermAST("Person_2", is_var=True)])],
                                                 conditions=[
                                                     ASTs.ConditionAST(ASTs.TermAST("Person", is_var=True),
                                                                       operator="=",
                                                                       rhs=ASTs.TermAST("Person_2", is_var=True))
                                                     ],
                                                 annotation=ASTs.RuleEnum.generates,
                                                 ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive(Person) generates breathing(Person_2) if [condition] (in )",
            "%% Ex Event generates Inst Event:",
            "occurred(breathing(Person_2), simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, ex),",
            "eventType(breathing(Person_2), simple, inst),",
            "holdsat(deontic(power, breathing(Person_2)), simple, I),",
            "observed(alive(Person), I),",
            "Person=Person_2, person(Person), person(Person_2), true.",
            "",
            "%% Inst Event Generates Inst Event",
            "occurred(breathing(Person_2), simple, I)            :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, inst),",
            "eventType(breathing(Person_2), simple, inst),",
            "holdsat(deontic(power, breathing(Person_2)), simple, I),",
            "occurred(alive(Person), simple, I),",
            "Person=Person_2, person(Person), person(Person_2), true.",
            "",
            "%% Unempowered event generation",
            "occurred(_unempoweredEvent(breathing(Person_2)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, ex),",
            "eventType(breathing(Person_2), simple, inst),",
            "not holdsat(deontic(power, breathing(Person_2)), simple, I),",
            "observed(alive(Person), I),",
            "Person=Person_2, person(Person), person(Person_2), true.",
            "",
            "occurred(_unempoweredEvent(breathing(Person_2)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(alive(Person), simple, inst),",
            "eventType(breathing(Person_2), simple, inst),",
            "not holdsat(deontic(power, breathing(Person_2)), simple, I),",
            "occurred(alive(Person), simple, I),",
            "Person=Person_2, person(Person), person(Person_2), true.",
            "",
            "%% Unpermitted event generation",
            "occurred(_unpermittedEvent(breathing(Person_2)), simple, I) :- instant(I),",
            "institution(simple),",
            "eventType(breathing(Person_2), simple, inst),",
            "holdsat(deontic(power, breathing(Person_2)), simple, I),",
            "not holdsat(deontic(permitted, breathing(Person_2)), simple, I),",
            "occurred(breathing(Person_2), simple, I),",
            "Person=Person_2, person(Person), person(Person_2), true.",
            "",
        ]

        for x,y in zip(result, expected):
            assert(x.strip() == y)

        assert(len(result) ==  len(expected))

    def test_generation_initiates(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("alive"),
                                                   [ASTs.TermAST("breathing")],
                                                   annotation=ASTs.RuleEnum.initiates,
                                                 ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive initiates breathing if [condition]",
            "initiated(breathing, simple, I) :- instant(I),",
            "institution(simple),",
            "inertialFluent(breathing, simple),",
            "holdsat(live(simple), simple, I),",
            "occurred(alive, simple, I),",
            "not occurred(violation(alive), simple, I),",
            "true.",
            "",
        ]

        for x,y in zip(result, expected):
            assert(x.strip() == y)

        assert(len(result) ==  len(expected))

    def test_generation_terminates(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("alive"),
                                               [ASTs.TermAST("breathing")],
                                               annotation=ASTs.RuleEnum.terminates,
                                               ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive terminates breathing if [condition]",
            "terminated(breathing, simple, I) :- instant(I),",
            "institution(simple),",
            "inertialFluent(breathing, simple),",
            "holdsat(live(simple), simple, I),",
            "occurred(alive, simple, I),",
            "not occurred(violation(alive), simple, I),",
            "true.",
            "",
        ]

        for x,y in zip(result, expected):
            assert(x.strip() == y)

        assert(len(result) ==  len(expected))

    def test_transient_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.TransientRuleAST(None,
                                                [ASTs.TermAST("alive")],
                                                [ASTs.ConditionAST(ASTs.TermAST("breathing"))],
                                                annotation=ASTs.RuleEnum.transient
                                                ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive when holdsat(breathing, simple, I), true",
            "holdsat(alive, simple, I) :- instant(I),",
            "institution(simple),",
            "transientFluent(alive, simple),",
            "holdsat(breathing, simple, I), true.",
            "",
        ]

        for x,y in zip(result, expected):
            assert(x.strip() == y)

        assert(len(result) ==  len(expected))

    def test_transient_with_types(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.rules.append(ASTs.TransientRuleAST(None,
                                                [ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)])],
                                                [ASTs.ConditionAST(ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)]))],
                                                annotation=ASTs.RuleEnum.transient
                                                ))

        compiler.compile_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive(Person) when holdsat(breathing(Person), simple, I), person(Person), true",
            "holdsat(alive(Person), simple, I) :- instant(I),",
            "institution(simple),",
            "transientFluent(alive(Person), simple),",
            "holdsat(breathing(Person), simple, I), person(Person), true.",
            "",
        ]

        for x,y in zip(result, expected):
            assert(x.strip() == y)

        assert(len(result) ==  len(expected))

    def test_full_institution(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))

        ##-- types
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Person")))
        inst.types.append(ASTs.DomainSpecAST(ASTs.TermAST("Book")))
        ##-- end types

        ##-- events
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet",
                                                      [ASTs.TermAST("Person_1",
                                                                    is_var=True),
                                                       ASTs.TermAST("Person_2",
                                                                    is_var=True)]),
                                         ASTs.EventEnum.violation))

        inst.events.append(ASTs.EventAST(ASTs.TermAST("arrive"),
                                         ASTs.EventEnum.institutional))

        inst.events.append(ASTs.EventAST(ASTs.TermAST("insult"),
                                         ASTs.EventEnum.violation))
        ##-- end events

        ##-- fluents
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive",
                                                        [ASTs.TermAST("Person",
                                                                      is_var=True)]),
                                           ASTs.FluentEnum.inertial))

        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("avenge",
                                                        [ASTs.TermAST("oblTest"),
                                                         ASTs.TermAST("deadTest"),
                                                         ASTs.TermAST("violTest"),
                                                         ]),
                                           ASTs.FluentEnum.achievement_obligation))

        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive"),
                                           ASTs.FluentEnum.transient))
        ##-- end fluents

        ##-- rules
        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                               [ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)])],
                                               annotation=ASTs.RuleEnum.generates,
                                                 ))

        inst.rules.append(ASTs.GenerationRuleAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                       [ASTs.TermAST("breathing", [ASTs.TermAST("Person_2", is_var=True)])],
                                       conditions=[
                                           ASTs.ConditionAST(ASTs.TermAST("Person", is_var=True),
                                                             operator="=",
                                                             rhs=ASTs.TermAST("Person_2", is_var=True))
                                       ],
                                       annotation=ASTs.RuleEnum.generates,
                                                 ))

        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("alive"),
                                               [ASTs.TermAST("breathing")],
                                               annotation=ASTs.RuleEnum.initiates,
                                               ))

        inst.rules.append(ASTs.InertialRuleAST(ASTs.TermAST("alive"),
                                               [ASTs.TermAST("breathing")],
                                               annotation=ASTs.RuleEnum.terminates,
                                               ))

        inst.rules.append(ASTs.TransientRuleAST(None,
                                                [ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)])],
                                                [ASTs.ConditionAST(ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)]))],
                                                annotation=ASTs.RuleEnum.transient,
                                                ))
        ##-- end rules

        result = compiler.compile([inst])
        assert(isinstance(result, str))
