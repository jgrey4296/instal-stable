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
semi    = (lit(";") + pp.line_end).suppress()

event_kws      = pp.MatchFirst(kw(x) for x in ["exogenous", "institutional", "violation", "ex", "inst", "viol"])
fluent_kws     = pp.MatchFirst(kw(x) for x in ["cross", "noninertial", "obligation", "x", "transient", "obl"])
generation_kws = pp.MatchFirst(kw(x) for x in ["generates", "xgenerates"])
inertial_kws   = pp.MatchFirst(kw(x) for x in ["initiates", "terminates", "xinitiates", "xterminates"])
op_lits        = pp.MatchFirst(lit(x) for x in ["<=", ">=", "<>", "!=", "<", ">", "=", ])

##-- end util

##-- constructors
def build_institution(string, loc, toks):
    inst = toks['head']
    body = toks['body']
    for elem in body:
        match elem:
            case ASTs.FluentAST():
                inst.fluents.append(elem)
            case ASTs.EventAST():
                inst.events.append(elem)
            case ASTs.TypeAST():
                inst.types.append(elem)
            case ASTs.RelationalAST():
                inst.relations.append(elem)
            case ASTs.TransientFluentRuleAST():
                inst.transient_rules.append(elem)
            case ASTs.InitiallyAST():
                inst.initial.append(elem)
            case ASTs.SourceAST():
                inst.sources.append(elem.head)
            case ASTs.SinkAST():
                inst.sinks.append(elem.head)

    return inst




def build_term(string, loc, toks) -> ASTs.TermAST:
    is_var, value = toks['value']
    return ASTs.TermAST(value,
                        params=toks['params'][:] if 'params' in toks else [],
                        is_var=is_var)


def build_fluent(string, loc, toks) -> ASTs.FluentAST:
    head     = toks['head']
    anno_str = toks.annotation
    match anno_str:
        case "cross":
            annotation = ASTs.FluentEnum.cross
        case "noninertial":
            annotation = ASTs.FluentEnum.transient
        case "transient":
            annotation = ASTs.FluentEnum.transient
        case "obligation":
            annotation = ASTs.FluentEnum.obligation
            assert(len(head.params) == 4), "Obligation Fluents need a requirement, deadline, violation, and repeat"
        case _:
            annotation = ASTs.FluentEnum.inertial

    return ASTs.FluentAST(head, annotation)


def build_event(string, loc, toks) -> ASTs.EventAST:
    head     = toks['head']
    anno_str = toks.annotation
    match anno_str:
        case "exogenous":
            annotation = ASTs.EventEnum.exogenous
        case "inst":
            annotation = ASTs.EventEnum.institutional
        case "violation":
            annotation = ASTs.EventEnum.violation

    return ASTs.EventAST(head, annotation)

def build_generate_rule(string, loc, toks) -> ASTs.GenerationRuleAST:
    head       = toks['head']
    body       = toks['body'][:]
    conditions = toks['conditions'] if 'conditions' in toks else []

    match toks['annotation']:
        case "xgenerates":
            annotation = ASTs.RuleEnum.xgenerates
        case "generates":
            annotation = ASTs.RuleEnum.generates
        case _:
            raise Exception("Not Recognised consequence relation: %s", toks['annotation'])

    return ASTs.GenerationRuleAST(head,
                                  body,
                                  conditions
                                  annotation=annotation
                                  )


    pass
def build_inertial_rule(string, loc, toks) -> ASTs.InertialRuleAST:
    head       = toks['head']
    body       = toks['body'][:]
    conditions = toks['conditions'] if 'conditions' in toks else []

    match toks['annotation']:
        case "xinitiates":
            annotation = ASTs.RuleEnum.xinitiates
        case "initiates":
            annotation = ASTs.RuleEnum.initiates
        case "xterminates":
            annotation = ASTs.RuleEnum.xterminates
        case "terminates":
            annotation = ASTs.RuleEnum.terminates
        case _:
            raise Exception("Not Recognised consequence relation: %s", toks['annotation'])

    return ASTs.InertialRuleAST(head,
                                body,
                                conditions,
                                annotation=annotation
                                )


def build_transient_rule(string, loc, toks) -> ASTs.TransientRuleAST:
    return ASTs.TransientRuleAST(toks['head'],
                                 [],
                                 toks['conditions'],
                                 annotation=ASTs.RuleEnum.transient)

##-- end constructors

##-- term parser
name = pp.Word(pp.alphas.lower(), pp.alphanums + "_")
name.set_parse_action(lambda s, l, t: (False, t[0]))
name.set_name("name")
# TODO: handle explicit type annotation
# TODO: handle numbers
var       = pp.Word(pp.alphas.upper(), pp.alphanums)
var.set_parse_action(lambda s, l, t: (True, t[0]))
var.set_name("var")

# The core Term parser:
TERM      = pp.Forward()
term_list = pp.delimited_list(op(ln) + TERM)

TERM  <<= (var | name)("value") + op(lit("(") + term_list("params") + lit(")"))
TERM.set_parse_action(build_term)
TERM.set_name("term")

in_inst       = s_kw('in') + TERM('inst')
##-- end term parser

##-- rules
CONDITION   = op(kw("not"))("not") + TERM("head")
CONDITION.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['head'], True if 'not' in t else False))
CONDITION.set_name("condition")

COMPARISON  = TERM("lhs") + op_lits("op") + TERM("rhs")
COMPARISON.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['lhs'], False, operator=t['op'], rhs=t['rhs']))

# TODO handle 'in {time}'
CONDITIONS  = pp.delimited_list(op(ln) + (COMPARISON | CONDITION))

GEN_RULE       = (TERM("head")
               + generation_kws("annotation")
               + term_list("body") + op(op(ln) + s_kw("if") + CONDITIONS)("conditions") + semi)
GEN_RULE.set_parse_action(build_generate_rule)
GEN_RULE.set_name("event generation rule")

INERTIAL_RULE  = (TERM("head")
               + inertial_kws("annotation")
               + term_list("body") + op(op(ln) + s_kw("if") + CONDITIONS)("conditions") + semi)
INERTIAL_RULE.set_parse_action(build_inertial_rule)
INERTIAL_RULE.set_name("inertial fluent rule")

TRANSIENT_RULE  = TERM("head") + s_kw("when") + CONDITIONS("conditions") + semi
TRANSIENT_RULE.set_parse_action(build_transient_rule)
TRANSIENT_RULE.set_name("transient rule")

RULE = GEN_RULE | INERTIAL_RULE | TRANSIENT_RULE

##-- end rules

##-- parser components
TYPE_DEC    = s_kw("type") + TERM('head') + semi
TYPE_DEC.set_parse_action(lambda s, l, t: ASTs.TypeAST(t['head']))
TYPE_DEC.set_name("type_dec")

FLUENT      = op(fluent_kws)("annotation") + s_kw("fluent") + TERM("head") + semi
FLUENT.set_parse_action(build_fluent)
FLUENT.set_name("fluent")

EVENT       = event_kws('annotation')  + s_kw("event")  + TERM("head") + semi
EVENT.set_parse_action(build_event)
EVENT.set_name("event")


INITIALLY   = s_kw("initially") + term_list("body") + op(s_kw("if") + CONDITIONS)("conditions") + semi
INITIALLY.set_parse_action(lambda s, l, t: ASTs.InitiallyAST(t['body'][:], t.conditions[:]))
INITIALLY.set_name("initially")
##-- end parser components

##-- institution
INSTITUTION = s_kw("institution") + TERM("head") + semi
INSTITUTION.set_parse_action(lambda s, l, t: ASTs.InstitutionDefAST(t['head'][0]))
INSTITUTION.set_name("institution")
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
institution_structure.set_parse_action(build_institution)

top_institution = orm(institution_structure)
top_institution.ignore(comment)

bridge_structure = (BRIDGE('head')
                    + zrm(SOURCE
                          | SINK
                          | TYPE_DEC
                          | EVENT
                          | FLUENT
                          | RULE
                          | INITIALLY)('body'))

bridge_structure.set_parse_action(build_institution)

top_bridge = orm(bridge_structure)
top_bridge.ignore(comment)

top_fact = orm(IAF_INITIALLY)
top_fact.ignore(comment)

top_query = orm(OBSERVED)
top_query.ignore(comment)

top_domain = orm(DOMAIN_SPEC)
top_domain.ignore(comment)
##-- end top level parser entry points
