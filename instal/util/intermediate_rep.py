#/usr/bin/env python3
"""
IR representations from parsed instal -> compiled clingo
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
##-- end imports

logging = logmod.getLogger(__name__)

@dataclass
class InstalIR:

    source : None|str = field(default=None, kw_only=True)

@dataclass
class IR_Program(InstalIR):
    institutions : list[InstalIR] = field(default_factory=list)
    bridges      : list[InstalIR] = field(default_factory=list)

@dataclass
class BridgeIR(InstalIR):
    source : str = field()
    sink   : str = field()

@dataclass
class InstitutionIR(InstalIR):
    name : str = field()

    fluents : list[InstalIR] = field()
    events  : list[InstalIR] = field()
    types   : list[InstalIR] = field()
