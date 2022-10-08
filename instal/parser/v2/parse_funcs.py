#/usr/bin/env python3,
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import pyparsing as pp
import instal.interfaces.ast as ASTs
import instal.parser.v2.constructors as construct

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- util
pp.ParserElement.set_default_whitespace_chars(" \t")

s       = pp.Suppress
op      = pp.Optional
orm     = pp.OneOrMore
zrm     = pp.ZeroOrMore
kw      = pp.Keyword
lit     = pp.Literal
gr      = lambda x: pp.Group(x)
s_kw    = lambda x: pp.Keyword(x).suppress()
s_lit   = lambda x: pp.Literal(x).suppress()
ln      = orm(pp.White("\n\r").set_whitespace_chars("\t ")).suppress()
ln.set_name("ln")
comment = pp.Regex(r"%.+?\n")
semi    = s(op(lit(";")) + pp.line_end)
semi.set_name(";")

event_kws      = pp.MatchFirst(kw(x) for x in ["exogenous", "institutional", "violation", "exo", "inst", "viol"])
fluent_kws     = pp.MatchFirst(kw(x) for x in ["cross", "obligation", "x", "transient", "obl"])
generation_kws = pp.MatchFirst(kw(x) for x in ["generates", "xgenerates"])
inertial_kws   = pp.MatchFirst(kw(x) for x in ["initiates", "terminates", "xinitiates", "xterminates"])
op_lits        = pp.MatchFirst(lit(x) for x in ["<=", ">=", "<>", "!=", "<", ">", "=", ])

##-- end util

##-- term parser
name = pp.Word(pp.alphas.lower() + "_", pp.alphanums + "_")
name.set_parse_action(lambda s, l, t: (False, t[0]))
name.set_name("name")
# TODO: handle explicit type annotation
var       = pp.Word(pp.alphas.upper(), pp.alphanums)
var.set_parse_action(lambda s, l, t: (True, t[0]))
var.set_name("var")

num = pp.common.signed_integer.copy()
num.add_parse_action(lambda s, l, t: (False, t[0]))

# The core Term parser:
TERM      = pp.Forward()
TERM.set_name("term")
term_list = pp.delimited_list(op(ln) + TERM)
term_list.set_name("Term Parameters")

# Number's can't actually be the value, only params,
# but we'll ensure that in a check heuristic
TERM  <<= (var | name | num)("value") + op(lit("(") + term_list("params") + lit(")"))
TERM.set_parse_action(construct.term)
TERM.set_name("term")

in_inst       = s_kw('in') + TERM('inst')
##-- end term parser

##-- rules
CONDITION   = op(kw("not"))("not") + TERM("head")
CONDITION.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['head'], True if 'not' in t else False))
CONDITION.set_name("condition")

COMPARISON  = TERM("lhs") + op_lits("op") + TERM("rhs")
COMPARISON.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['lhs'], False, operator=t['op'], rhs=t['rhs']))
COMPARISON.set_name("comparison")

# TODO handle 'in {time}'
CONDITIONS  = pp.delimited_list(op(ln) + (COMPARISON | CONDITION))
CONDITIONS.set_name("Condition list")

GEN_RULE       = (TERM("head")
               + generation_kws("annotation")
               + term_list("body") + op(op(ln) + s_kw("if") + CONDITIONS)("conditions") + semi)
GEN_RULE.set_parse_action(construct.generate_rule)
GEN_RULE.set_name("event generation rule")

INERTIAL_RULE  = (TERM("head")
               + inertial_kws("annotation")
               + term_list("body") + op(op(ln) + s_kw("if") + CONDITIONS)("conditions") + semi)
INERTIAL_RULE.set_parse_action(construct.inertial_rule)
INERTIAL_RULE.set_name("inertial fluent rule")

TRANSIENT_RULE  = TERM("head") + s_kw("when") + CONDITIONS("conditions") + semi
TRANSIENT_RULE.set_parse_action(construct.transient_rule)
TRANSIENT_RULE.set_name("transient rule")

RULE = GEN_RULE | INERTIAL_RULE | TRANSIENT_RULE

##-- end rules

##-- parser components
TYPE_DEC    = s_kw("type") + TERM('head') + semi
TYPE_DEC.set_parse_action(lambda s, l, t: ASTs.TypeAST(t['head']))
TYPE_DEC.set_name("type_dec")

FLUENT      = op(fluent_kws)("annotation") + s_kw("fluent") + TERM("head") + semi
FLUENT.set_parse_action(construct.fluent)
FLUENT.set_name("fluent")

EVENT       = event_kws('annotation')  + s_kw("event")  + TERM("head") + semi
EVENT.set_parse_action(construct.event)
EVENT.set_name("event")


INITIALLY   = s_kw("initially") + term_list("body") + op(s_kw("if") + CONDITIONS)("conditions") + semi
INITIALLY.set_parse_action(lambda s, l, t: ASTs.InitiallyAST(t['body'][:], t.conditions[:]))
INITIALLY.set_name("initially")
##-- end parser components

##-- institution
INSTITUTION = s_kw("institution") + TERM("head") + semi
INSTITUTION.set_parse_action(lambda s, l, t: ASTs.InstitutionDefAST(t['head'][0]))
INSTITUTION.set_name("institution head")
##-- end institution

##-- bridge specific
BRIDGE      = s_kw("bridge") + TERM("head") + semi
BRIDGE.set_parse_action(lambda s, l, t: ASTs.BridgeDefAST(t['head'][0]))

SINK        = s_kw("sink") + TERM("head") + semi
SINK.set_parse_action(lambda s, l, t: ASTs.SinkAST(t['head']))

SOURCE      = s_kw("source") + TERM("head") + semi
SOURCE.set_parse_action(lambda s, l, t: ASTs.SourceAST(t['head']))
##-- end bridge specific

##-- idc domain
DOMAIN_SPEC = TERM('head') + s_lit(":") + orm(TERM)("body") + pp.line_end
DOMAIN_SPEC.set_parse_action(lambda s, l, t: ASTs.DomainSpecAST(t['head'], t['body'][:]))
##-- end idc domain

##-- iaf facts / situation
cond_list     = op(s_kw("if") + CONDITIONS)("conditions")
IAF_INITIALLY = s_kw("initially") + TERM("body") + in_inst + cond_list + pp.line_end
IAF_INITIALLY.set_parse_action(lambda s, l, t: ASTs.InitiallyAST([t['body']], t.conditions[:], inst=t['inst']))
##-- end iaf facts / situation

##-- iaq query specification
OBSERVED = s_kw('observed') + TERM('fact') + op(s_kw('at') + pp.common.integer('time')) + pp.line_end
# OBSERVED.set_parse_action(lambda s, l, t: breakpoint())
OBSERVED.set_parse_action(lambda s, l, t: ASTs.QueryAST(t['fact'], time=t.time if t.time != '' else None))
##-- end iaq query specification

##-- top level parser entry points
institution_structure = (INSTITUTION('head')
                         + zrm(ln
                               | TYPE_DEC
                               | EVENT
                               | FLUENT
                               | RULE
                               | INITIALLY) ('body'))
institution_structure.set_parse_action(construct.institution)
institution_structure.set_name("Institution Structure")

top_institution = orm(institution_structure)
top_institution.ignore(comment)
top_institution.set_name("Institutions")

bridge_structure = (BRIDGE('head')
                    + zrm(SOURCE
                          | SINK
                          | TYPE_DEC
                          | EVENT
                          | FLUENT
                          | RULE
                          | INITIALLY)('body'))

bridge_structure.set_parse_action(construct.institution)
bridge_structure.set_name("Bridge Structure")

top_bridge = orm(bridge_structure)
top_bridge.ignore(comment)
top_bridge.set_name("Bridges")

top_fact = orm(IAF_INITIALLY)
top_fact.ignore(comment)
top_fact.set_name("Initial Facts")

top_query = orm(OBSERVED)
top_query.ignore(comment)
top_query.set_name("Queries")

top_domain = orm(DOMAIN_SPEC)
top_domain.ignore(comment)
top_domain.set_name("Domain Specifications")
##-- end top level parser entry points
