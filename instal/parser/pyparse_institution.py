#/usr/bin/env python3,
"""
,
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
from instal.interfaces.parser import InstalParser
import instal.interfaces.ast as ASTs

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- util
s         = pp.Suppress
op        = pp.Optional
orm       = pp.OneOrMore
zrm       = pp.ZeroOrMore
kw        = pp.Keyword
lit       = pp.Literal
##-- end util

##-- constructors
def build_term(string, loc, toks):
    is_var, head = toks['head']
    return ASTs.TermAST(head,
                      params=toks['params'][:] if 'params' in toks else [],
                      is_var=is_var)


def build_fluent(string, loc, toks):
    head     = toks['head']
    anno_str = toks['annotation'] if 'annotation' in toks else None
    match anno_str:
        case "cross":
            annotation = ASTs.FluentEnum.cross
        case "noninertial":
            annotation = ASTs.FluentEnum.noninertial
        case "obligation":
            annotation = ASTs.FluentEnum.obligation
        case _:
            annotation = None

    return ASTs.FluentAST(head, annotation)

def build_event(string, loc, toks):
    head     = toks['head']
    anno_str = toks['annotation'] if 'annotation' in toks else None
    match anno_str:
        case "exogenous":
            annotation = ASTs.EventEnum.exogenous
        case "inst":
            annotation = ASTs.EventEnum.institutional
        case "violation":
            annotation = ASTs.EventEnum.violation
        case _:
            annotation = None

    return ASTs.EventAST(head, annotation)

def build_relation(string, loc, toks):
    head       = toks['head']
    body       = toks['body'][:]
    conditions = toks['conditions'] if 'conditions' in toks else []

    match toks['annotation']:
        case "xgenerates":
            annotation = ASTs.RelationalEnum.xgenerates
        case "generates":
            annotation = ASTs.RelationalEnum.generates
        case "xinitiates":
            annotation = ASTs.RelationalEnum.xinitiates
        case "initiates":
            annotation = ASTs.RelationalEnum.initiates
        case "xterminates":
            annotation = ASTs.RelationalEnum.xterminates
        case "terminates":
            annotation = ASTs.RelationalEnum.terminates
        case _:
            raise Exception("Not Recognised consequence relation: %s", toks['annotation'])

    return ASTs.RelationalAST(head,
                            annotation,
                            body,
                            conditions)

##-- end constructors

##-- parser components
comment      = pp.Regex(r"%.+?")
semi         = lit(";").suppress()
fluent_kws   = pp.MatchFirst([kw(x) for x in ["cross", "noninertial", "obligation"]])
event_kws    = pp.MatchFirst([kw(x) for x in ["exogenous", "inst", "violation"]])
relation_kws = pp.MatchFirst([kw(x) for x in ["generates", "initiates", "terminates",
                                "xgenerates", "xinitiates", "xterminates"]])

name = pp.Word(pp.alphanums)
name.set_parse_action(lambda s, l, t: (False, t[0]))
var       = pp.Word(pp.alphas.upper(), pp.alphanums)
var.set_parse_action(lambda s, l, t: (True, t[0]))

# The core Term parser:
term      = pp.Forward()
term_list = pp.delimited_list(term)

term  <<= (var | name)("head") + op(lit("(") + term_list("params") + lit(")"))
term.set_parse_action(build_term)
term.set_name("term")

# Statements:
type_dec    = kw("type").suppress() + term('head') + semi
type_dec.set_parse_action(lambda s, l, t: ASTs.TypeAST(t['head']))

domain_spec = term('head') + lit(":").suppress() + orm(term)("body")
domain_spec.set_parse_action(lambda s, l, t: ASTs.DomainSpecAST(t['head'], t['body'][:]))

fluent = op(fluent_kws)("annotation") + kw("fluent").suppress() + term("head") + semi
fluent.set_parse_action(build_fluent)

event  = op(event_kws)('annotation')  + kw("event").suppress()  + term("head") + semi
event.set_parse_action(build_event)

condition = op(kw("not"))("not") + term("head")
condition.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['head'], True if 'not' in t else False))

conditions = kw("if").suppress() + pp.delimited_list(condition)

relation  = (term("head")
            + relation_kws("annotation")
            + term_list("body") + op(conditions)("conditions") + semi)
relation.set_parse_action(build_relation)

obligation = term("head") + kw("when").suppress() + term_list("body") + semi
obligation.set_parse_action(lambda s, l, t: ASTs.ObligationAST(t['head'], t['body'][:]))

initially = kw("initially").suppress() + term_list("body") + semi
initially.set_parse_action(lambda s, l, t: ASTs.InitiallyAST(t['body'][:]))

institution = kw("institution").suppress() + term("head") + semi
institution.set_parse_action(lambda s, l, t: ASTs.InstitutionDefAST(t['head']))

bridge = kw("bridge").suppress() + term("head") + semi
bridge.set_parse_action(lambda s, l, t: ASTs.BridgeDefAST(t['head']))

sink   = kw("sink").suppress() + term("head") + semi
sink.set_parse_action(lambda s, l, t: ASTs.SinkAST(t['head']))

source = kw("source").suppress() + term("head") + semi
source.set_parse_action(lambda s, l, t: ASTs.SourceAST(t['head']))
##-- end parser components

##-- top level parser entry points
top_institution = (institution
                   + orm(type_dec
                         | event
                         | fluent
                         | relation
                         | initially))
top_institution.ignore(comment)

top_bridge = (bridge
              + orm(source
                    | sink
                    | type_dec
                    | event
                    | fluent
                    | relation
                    | initially))
top_bridge.ignore(comment)

top_fact = orm(initially)
top_fact.ignore(comment)

top_atom = orm(term)
##-- end top level parser entry points

##-- interface implementation
class InstalPyParser(InstalParser):


    def parse_institution(self, text:str) -> ASTs.InstalAST:
        """ Mainly for .ial's """
        # TODO group results
        return top_institution.parse_string(text, parse_all=True)[0]

    def parse_bridge(self, text:str) -> ASTs.InstalAST:
        """ Mainly for .iab's """
        # TODO group results
        return top_brige.parse_string(text, parse_all=True)[0]

    def parse_facts(self, text:str) -> list[ASTs.InstalAST]:
        """ Mainly for .iaf's """
        return top_fact.parse_string(text, parse_all=True)[:]

    def parse_atoms(self, text:str) -> list[ASTs.InstalAST]:
        """ Mainly for parsing json fragment for traces """
        return term.parse_string(text, parse_all=True)[:]


##-- end interface implementation
