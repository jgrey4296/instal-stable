#/usr/bin/env python3
"""
AST representations from parsed instal -> compiled clingo
"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from enum import Enum, auto
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref
##-- end imports

__all__ = [
    "EventEnum", "FluentEnum", "RelationalEnum", "InstalAST",
    "TermAST", "ModelAST", "DomainTotalityAST", "QueryTotalityAST",
    "FactTotalityAST", "TypeTotalityAST", "InstitutionDefAST",
    "BridgeDefAST", "DomainSpecAST", "QueryAST", "InitiallyAST",
    "TypeAST", "EventAST", "FluentAST", "ConditionAST",
    "RelationalAST", "NifRuleAST", "SinkAST", "SourceAST",
]
logging = logmod.getLogger(__name__)

##-- enums
class EventEnum(Enum):
    exogenous     = auto()
    institutional = auto()
    violation     = auto()

class FluentEnum(Enum):
    inertial    = auto()
    noninertial = auto()
    obligation  = auto()
    cross       = auto()

class RelationalEnum(Enum):
    generates   = auto()
    initiates   = auto()
    terminates  = auto()
    xgenerates  = auto()
    xinitiates  = auto()
    xterminates = auto()

##-- end enums

##-- core base asts
@dataclass(frozen=True)
class InstalAST:
    parse_source : list[str] = field(default_factory=list, kw_only=True)

    @property
    def sources_str(self):
        return " ".join(str(x) for x in self.parse_source)

@dataclass(frozen=True)
class TermAST(InstalAST):
    value  : str             = field()
    params : list[InstalAST] = field(default_factory=list)
    is_var : bool            = field(default=False)

    def __str__(self):
        if bool(self.params):
            param_str = ", ".join(str(x) for x in self.params)
            return self.value + "(" + param_str + ")"

        return str(self.value)

    def __eq__(self, other):
        if not self.value == other.value:
            return False

        return all(x == y for x,y in zip(self.params, other.params))


##-- end core base asts

##-- top level collection asts
@dataclass(frozen=True)
class ModelAST(InstalAST):
    """
    Combines institutions and bridges together
    """
    institutions : list[InstalAST] = field(default_factory=list)
    bridges      : list[InstalAST] = field(default_factory=list)


@dataclass(frozen=True)
class DomainTotalityAST(InstalAST):
    body : list[DomainSpecAST] = field(default_factory=list)

    def __len__(self):
        return len(self.body)

@dataclass(frozen=True)
class QueryTotalityAST(InstalAST):
    body : list[QueryAST] = field(default_factory=list)

    def __len__(self):
        return len(self.body)

@dataclass(frozen=True)
class FactTotalityAST(InstalAST):
    body : list[InitiallyAST] = field(default_factory=list)

    def __len__(self):
        return len(self.body)

@dataclass(frozen=True)
class TypeTotalityAST(InstalAST):
    body : list[TypeAST] = field(default_factory=list)

    def __len__(self):
        return len(self.body)
##-- end top level collection asts

##-- institutions and bridges
@dataclass(frozen=True)
class InstitutionDefAST(InstalAST):
    head      : TermAST             = field()
    fluents   : list[FluentAST]     = field(default_factory=list)
    events    : list[EventAST]      = field(default_factory=list)
    types     : list[TypeAST]       = field(default_factory=list)
    relations : list[RelationalAST] = field(default_factory=list)
    nif_rules : list[NifRuleAST]    = field(default_factory=list)
    initial   : list[InitiallyAST]  = field(default_factory=list)

@dataclass(frozen=True)
class BridgeDefAST(InstitutionDefAST):
    sources   : list[TermAST]         = field(default_factory=list)
    sinks     : list[TermAST]         = field(default_factory=list)

##-- end institutions and bridges

##-- domain, query, facts
@dataclass(frozen=True)
class DomainSpecAST(InstalAST):
    """
    Type : instance, instance, instance;
    """
    head  : TermAST       = field()
    body  : list[TermAST] = field(default_factory=list)

@dataclass(frozen=True)
class QueryAST(InstalAST):
    head : TermAST      = field()
    inst : None|TermAST = field(default=None)
    time : None|int     = field(default=None)

@dataclass(frozen=True)
class InitiallyAST(InstalAST):
    body       : list[TermAST]      = field(default_factory=list)
    conditions : list[ConditionAST] = field(default_factory=list)
    inst       : None|TermAST       = field(default=None)
##-- end domain, query, facts

##-- specialised asts
@dataclass(frozen=True)
class TypeAST(InstalAST):
    head : TermAST = field()

@dataclass(frozen=True)
class EventAST(InstalAST):
    head       : TermAST   = field()
    annotation : EventEnum = field()

@dataclass(frozen=True)
class FluentAST(InstalAST):
    head       : TermAST    = field()
    annotation : FluentEnum = field(default=FluentEnum.inertial)


@dataclass(frozen=True)
class ConditionAST(InstalAST):
    head     : TermAST      = field()
    negated  : bool         = field(default=False)
    operator : None|str     = field(default=None)
    rhs      : None|TermAST = field(default=None)

@dataclass(frozen=True)
class RelationalAST(InstalAST):
    """
    for generation and consequence relations
    """
    head       : TermAST            = field()
    annotation : RelationalEnum     = field()
    body       : list[TermAST]      = field(default_factory=list)
    conditions : list[ConditionAST] = field(default_factory=list)
    delay      : int                = field(default=0)

@dataclass(frozen=True)
class NifRuleAST(InstalAST):
    head : TermAST       = field()
    body : list[ConditionAST] = field(default_factory=list)

@dataclass(frozen=True)
class SinkAST(InstalAST):
    head : TermAST = field()

@dataclass(frozen=True)
class SourceAST(InstalAST):
    head : TermAST = field()

##-- end specialised asts
