#/usr/bin/env python3
"""
IR representations from parsed instal -> compiled clingo
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

logging = logmod.getLogger(__name__)

##-- enums
class EventEnum(Enum):
    exogenous     = auto()
    institutional = auto()
    violation     = auto()
    creation      = auto()
    dissolution   = auto()
    cross         = auto()
    generates     = auto()
    initiates     = auto()
    terminates    = auto()
    initially     = auto()


class FluentEnum(Enum):
    inertial    = auto()
    noninertial = auto()
    power       = auto()
    permission  = auto()
    violation   = auto()
    obligation  = auto()
    cross       = auto()

class CrossEventEnum(Enum):
    generates = auto()
    initiates = auto()
    terminates = auto()
    xgenerates = auto()
    xinitiates = auto()
    xterminates = auto()

##-- end enums

##-- IRs
@dataclass
class InstalIR:

    source : None|str = field(default=None, kw_only=True)

@dataclass
class IR_Program(InstalIR):
    """
    Combines institutions and bridges together
    """
    institutions : list[InstalIR] = field(default_factory=list)
    bridges      : list[InstalIR] = field(default_factory=list)

@dataclass
class BridgeIR(InstalIR):
    name      : TermIR             = field()
    sources   : list[TermIR]       = field(default_factory=list)
    sinks     : list[TermIR]       = field(default_factory=list)
    relations : list[RelationalIR] = field(default_factory=list)
    fluents   : list[FluentIR]     = field(default_factory=list)

@dataclass
class InstitutionIR(InstalIR):
    name      : TermIR             = field()
    fluents   : list[InstalIR]     = field(default_factory=list)
    events    : list[EventIR]      = field(default_factory=list)
    types     : list[TypeIR]       = field(default_factory=list)
    relations : list[RelationalIR] = field(default_factory=list)


@dataclass
class TermIR(InstalIR):
    name   : str = field()
    params : list[InstalIR] = field(default_factory=list)
    is_var : bool = field(default=False)

@dataclass
class TypeIR(InstalIR):
    name : TermIR = field()

@dataclass
class DomainSpecIR(InstalIR):
    name  : TermIR       = field()
    terms : list[TermIR] = field(default_factory=list)

@dataclass
class EventIR(InstalIR):
    name    : TermIR    = field()
    variety : EventEnum = field()

@dataclass
class FluentIR(InstalIR):
    name    : TermIR     = field()
    variety : FluentEnum = field()


@dataclass
class RelationalIR(InstalIR):
    """
    for generation and consequence relations
    """
    head       : TermIR         = field()
    variety    : CrossEventEnum = field()
    body       : list[TermIR]   = field(default_factory=list)
    conditions : list[TermIR]   = field(default_factory=list)

@dataclass
class ObligationIR(InstalIR):
    head : TermIR       = field()
    body : list[TermIR] = field(default_factory=list)

@dataclass
class InitiallyIR(InstalIR):
    body : list[TermIR] = field(default_factory=list)

##-- end IRs
