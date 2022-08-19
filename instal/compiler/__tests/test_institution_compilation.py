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
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.interfaces import ast as ASTs
from unittest import mock
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

def null_event_text(inst_name:str):
    text = [
            "%% null event for unknown events",
            "% Event: null (type: ex)",
            "event(null).",
            "event(viol(null)).",
            "",
            "evtype(null, {0}, ex).",
            "evtype(viol(null), {0}, viol).",
            "",
            "evinst(null, {0}).",
            "evinst(viol(null), {0}).",
            "",
            "ifluent(pow(null), {0}).",
            "ifluent(perm(null), {0}).",
            "fluent(pow(null), {0}).",
            "fluent(perm(null), {0}).",
            "",
            "% no creation event",
            "holdsat(live({0}), {0}, I) :- start(I), inst({0}).",
            "holdsat(perm(null), {0}, I)    :- start(I), inst({0}).",
            "holdsat(pow(null), {0}, I)     :- start(I), inst({0}).",
            ""
        ]

    return [x.format(inst_name) for x in text]

class TestInstitutionCompiler(unittest.TestCase):
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


    def test_simple_institution(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))

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







    def test_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.exogenous))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: exogenous)",
            "event(greet)                       :- true.",
            "event(viol(greet))                 :- true.",
            "",
            "evtype(greet, simple, ex)         :- true.",
            "evtype(viol(greet), simple, viol) :- true.",
            "",
            "evinst(greet, simple)             :- true.",
            "evinst(viol(greet), simple)       :- true.",
            "",
            "fluent(pow(greet), simple)        :- true.",
            "fluent(perm(greet), simple)       :- true.",
            "",
            "ifluent(pow(greet), simple)       :- true.",
            "ifluent(perm(greet), simple)      :- true.",
            "",
            ] + null_event_text("simple")
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

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
            "% Event: greet (type: exogenous)",
            "event(greet)                       :- true.",
            "event(viol(greet))                 :- true.",
            "",
            "evtype(greet, simple, ex)         :- true.",
            "evtype(viol(greet), simple, viol) :- true.",
            "",
            "evinst(greet, simple)             :- true.",
            "evinst(viol(greet), simple)       :- true.",
            "",
            "fluent(pow(greet), simple)        :- true.",
            "fluent(perm(greet), simple)       :- true.",
            "",
            "ifluent(pow(greet), simple)       :- true.",
            "ifluent(perm(greet), simple)      :- true.",
            "",
            "% Event: accuse (type: exogenous)",
            "event(accuse)                       :- true.",
            "event(viol(accuse))                 :- true.",
            "",
            "evtype(accuse, simple, ex)         :- true.",
            "evtype(viol(accuse), simple, viol) :- true.",
            "",
            "evinst(accuse, simple)             :- true.",
            "evinst(viol(accuse), simple)       :- true.",
            "",
            "fluent(pow(accuse), simple)        :- true.",
            "fluent(perm(accuse), simple)       :- true.",
            "",
            "ifluent(pow(accuse), simple)       :- true.",
            "ifluent(perm(accuse), simple)      :- true.",
            "",
            ] + null_event_text("simple")
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)





    def test_inst_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.institutional))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: institutional)",
            "event(greet)                       :- true.",
            "event(viol(greet))                 :- true.",
            "",
            "evtype(greet, simple, inst)       :- true.",
            "evtype(viol(greet), simple, viol) :- true.",
            "",
            "evinst(greet, simple)             :- true.",
            "evinst(viol(greet), simple)       :- true.",
            "",
            "ifluent(perm(greet), simple)      :- true.",
            "fluent(perm(greet), simple)       :- true.",
            "",
            ] + null_event_text("simple")
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)





    def test_violation_event_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet"),
                                         ASTs.EventEnum.violation))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet (type: violation)",
            "event(greet)                 :- true.",
            "evtype(greet, simple, viol) :- true.",
            "evinst(greet, simple)       :- true.",
            "",
            ] + null_event_text("simple")
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)



    def test_events_with_types_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.events.append(ASTs.EventAST(ASTs.TermAST("greet",
                                                      [ASTs.TermAST("Person_1",
                                                                    is_var=True),
                                                       ASTs.TermAST("Person_2",
                                                                    is_var=True)]),
                                         ASTs.EventEnum.violation))

        compiler.compile_events(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Event: greet(Person_1, Person_2) (type: violation)",
            "event(greet(Person_1, Person_2))                 :- person(Person_1), person(Person_2), true.",
            "evtype(greet(Person_1, Person_2), simple, viol) :- person(Person_1), person(Person_2), true.",
            "evinst(greet(Person_1, Person_2), simple)       :- person(Person_1), person(Person_2), true.",
            "",
            ] + null_event_text("simple")
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)



    def test_fluent_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive"),
                                           ASTs.FluentEnum.inertial))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% inertial fluent: alive %",
            "ifluent(alive, simple) :- true.",
            "fluent(alive,  simple) :- true.",
            ""
        ]
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)


    def test_fluent_with_types_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive",
                                                        [ASTs.TermAST("Person",
                                                                      is_var=True)]),
                                           ASTs.FluentEnum.inertial))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% inertial fluent: alive(Person) %",
            "ifluent(alive(Person), simple) :- person(Person), true.",
            "fluent(alive(Person),  simple) :- person(Person), true.",
            ""
        ]
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)



    def test_fluent_obligation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("avenge",
                                                        [ASTs.TermAST("oblTest"),
                                                         ASTs.TermAST("deadTest"),
                                                         ASTs.TermAST("violTest")
                                                         ]),
                                           ASTs.FluentEnum.obligation))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% obligation fluent: avenge(oblTest, deadTest, violTest) %",
            "oblfluent(obl(oblTest, deadTest, violTest), simple)     :- inst(simple), event(violTest), true.",
            "ifluent(obl(oblTest, deadTest, violTest), simple)       :- inst(simple), event(violTest), true.",
            "fluent(obl(oblTest, deadTest, violTest), simple)        :- inst(simple), event(violTest), true.",
            "terminated(obl(oblTest, deadTest, violTest), simple, I) :- inst(simple), holdsat(obl(oblTest, deadTest, violTest), simple, I), event(violTest), true.",
            "terminated(obl(oblTest, deadTest, violTest), simple, I) :- inst(simple), holdsat(obl(oblTest, deadTest, violTest), simple, I), event(violTest), true.",
            "occurred(violTest, simple, I)                                    :- inst(simple), holdsat(obl(oblTest, deadTest, violTest), simple, I), event(violTest), true.",
            "",
        ]
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)



    def test_fluent_non_inertial(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.fluents.append(ASTs.FluentAST(ASTs.TermAST("alive"),
                                           ASTs.FluentEnum.noninertial))

        compiler.compile_fluents(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% noninertial fluent: alive %",
            "nifluent(alive, simple) :- true.",
            "fluent(alive,   simple) :- true.",
            ""
        ]
        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)


    def test_generation_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.relations.append(ASTs.RelationalAST(ASTs.TermAST("alive"),
                                                 ASTs.RelationalEnum.generates,
                                                 [ASTs.TermAST("breathing")]
                                                 ))

        compiler.compile_generation(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive generates breathing if [condition] (in )",
            "occurred(breathing, simple, I) :- occurred(alive, simple, I), inst(simple), instant(I), not occurred(viol(alive) simple, I), true.",
            "",
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

    def test_generation_with_types(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.relations.append(ASTs.RelationalAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                                 ASTs.RelationalEnum.generates,
                                                 [ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)])]
                                                 ))

        compiler.compile_generation(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive(Person) generates breathing(Person) if [condition] (in )",
            "occurred(breathing(Person), simple, I) :- occurred(alive(Person), simple, I), inst(simple), instant(I), not occurred(viol(alive(Person)) simple, I), person(Person), true.",
            "",
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)


    def test_generation_with_condition(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.relations.append(ASTs.RelationalAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                                 ASTs.RelationalEnum.generates,
                                                 [ASTs.TermAST("breathing", [ASTs.TermAST("Person_2", is_var=True)])],
                                                 conditions=[
                                                     ASTs.ConditionAST(ASTs.TermAST("Person", is_var=True),
                                                                       operator="=",
                                                                       rhs=ASTs.TermAST("Person_2", is_var=True))
                                                     ]
                                                 ))

        compiler.compile_generation(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "% Translation of alive(Person) generates breathing(Person_2) if [condition] (in )",
            "occurred(breathing(Person_2), simple, I) :- occurred(alive(Person), simple, I), inst(simple), instant(I), not occurred(viol(alive(Person)) simple, I), Person=Person_2, person(Person), person(Person_2), true.",
            "",
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

    def test_generation_initiates(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.relations.append(ASTs.RelationalAST(ASTs.TermAST("alive"),
                                                 ASTs.RelationalEnum.initiates,
                                                 [ASTs.TermAST("breathing")]
                                                 ))

        compiler.compile_generation(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive initiates breathing if [condition]",
            "initiated(breathing, simple, I) :- occurred(alive, simple, I), holdsat(live(simple), simple, I), inst(simple), instant(I), not occurred(viol(alive), simple, I), true.",
            "",
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)


    def test_generation_terminates(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.relations.append(ASTs.RelationalAST(ASTs.TermAST("alive"),
                                                 ASTs.RelationalEnum.terminates,
                                                 [ASTs.TermAST("breathing")]
                                                 ))

        compiler.compile_generation(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive terminates breathing if [condition]",
            "terminated(breathing, simple, I) :- occurred(alive, simple, I), holdsat(live(simple), simple, I), inst(simple), instant(I), not occurred(viol(alive), simple, I), true.",
            ""
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)



    def test_nif_compilation(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.nif_rules.append(ASTs.NifRuleAST(ASTs.TermAST("alive"),
                                              [ASTs.TermAST("breathing")]
                                              ))

        compiler.compile_nif_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive when breathing, true",
            "holdsat(alive, simple, I) :- inst(simple), instant(I), breathing, true.",
            ""
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

    def test_nif_with_types(self):
        compiler = InstalInstitutionCompiler()
        inst     = ASTs.InstitutionDefAST(ASTs.TermAST("simple"))
        inst.types.append(ASTs.TypeAST(ASTs.TermAST("Person")))
        inst.nif_rules.append(ASTs.NifRuleAST(ASTs.TermAST("alive", [ASTs.TermAST("Person", is_var=True)]),
                                              [ASTs.TermAST("breathing", [ASTs.TermAST("Person", is_var=True)])]
                                              ))

        compiler.compile_nif_rules(inst)
        result = ("\n".join(compiler._compiled_text[:])).split("\n")
        expected = [
            "%% Translation of alive(Person) when breathing(Person), person(Person), true",
            "holdsat(alive(Person), simple, I) :- inst(simple), instant(I), breathing(Person), person(Person), true.",
            ""
        ]

        self.assertEqual(len(result), len(expected))
        for x,y in zip(result, expected):
            self.assertEqual(x,y)

if __name__ == '__main__':
    unittest.main()
