#/usr/bin/env python3
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

##-- ast constructors
def institution(string, loc, toks):
    inst = toks['head']
    body = toks['body']
    for elem in body:
        match elem:
            case ASTs.FluentAST():
                inst.fluents.append(elem)
            case ASTs.EventAST():
                inst.events.append(elem)
            case ASTs.DomainSpecAST():
                inst.types.append(elem)
            case ASTs.RuleAST():
                inst.rules.append(elem)
            case ASTs.InitiallyAST():
                inst.initial.append(elem)
            case ASTs.BridgeLinkAST():
                inst.links.append(elem)

    return inst




def term(string, loc, toks) -> ASTs.TermAST:
    is_var, value = toks['value']
    return ASTs.TermAST(value,
                        params=toks['params'][:] if 'params' in toks else [],
                        is_var=is_var)


def fluent(string, loc, toks) -> ASTs.FluentAST:
    head     = toks['head']
    anno_str = toks.annotation
    match anno_str:
        case "cross":
            annotation = ASTs.FluentEnum.cross
        case "noninertial":
            annotation = ASTs.FluentEnum.transient
        case "obligation":
            annotation = ASTs.FluentEnum.obligation
            if len(head.params) != 3:
                raise pp.ParseFatalException(string, loc, "Obligation arguments need to be of the form a (requirement, deadline, violation)")

            head.params.append(ASTs.TermAST("achievement"))
        case _:
            annotation = ASTs.FluentEnum.inertial

    return ASTs.FluentAST(head, annotation)


def event(string, loc, toks) -> ASTs.EventAST:
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

def generate_rule(string, loc, toks) -> ASTs.GenerationRuleAST:
    head       = toks['head']
    body       = toks['body'][:]
    conditions = toks['conditions'][:] if 'conditions' in toks else []

    match toks['annotation']:
        case "xgenerates":
            annotation = ASTs.RuleEnum.xgenerates
        case "generates":
            annotation = ASTs.RuleEnum.generates
        case _:
            raise Exception("Not Recognised consequence relation: %s", toks['annotation'])

    return ASTs.GenerationRuleAST(head,
                                  body,
                                  conditions,
                                  annotation=annotation
                                  )


    pass
def inertial_rule(string, loc, toks) -> ASTs.InertialRuleAST:
    head       = toks['head']
    body       = toks['body'][:]
    conditions = toks['conditions'][:] if 'conditions' in toks else []

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


def transient_rule(string, loc, toks) -> ASTs.TransientRuleAST:
    return ASTs.TransientRuleAST(None,
                                 [toks['body']],
                                 toks['conditions'][:],
                                 annotation=ASTs.RuleEnum.transient)

##-- end ast constructors
