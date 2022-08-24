#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
from collections.abc import Sequence
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
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.ast import TermAST

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


logging = logmod.getLogger(__name__)


class State_Protocol(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __str__(self): pass

    @staticmethod
    @abc.abstractmethod
    def from_json(path): pass

    @staticmethod
    @abc.abstractmethod
    def from_model(model:InstalModelResult, step:int): pass

    @abc.abstractmethod
    def to_json(self) -> str: pass

    @abc.abstractmethod
    def to_ast(self) -> list[TermAST]: pass

    @abc.abstractmethod
    def check(self, conditions): pass

    @abc.abstractmethod
    def insert(self, val): pass

@dataclass
class State(State_Protocol):
    """
    Description of a single moment in a model's trace.
    """

    timestep : int          = field(default=0)
    metadata : dict         = field(default_factory=dict)
    holdsat  : list[Symbol] = field(default_factory=list)
    occurred : list[Symbol] = field(default_factory=list)
    observed : list[Symbol] = field(default_factory=list)


class Trace(Sequence):
    """
    The collected sequence of instance states which comprise
    a full model run
    """


    @abc.abstractmethod
    def __getitem__(self, index): pass
    @abc.abstractmethod
    def __len__(self): pass
    @abc.abstractmethod
    def __str__(self): pass

    @abc.abstractmethod
    def meets(self, conditions): pass
    @abc.abstractmethod
    def check(self, conditions): pass
    @abc.abstractmethod
    def append(self, data): pass
    @abc.abstractmethod
    def last(self): pass

    @abc.abstractmethod
    def to_json(self): pass
    @classmethod
    @abc.abstractmethod
    def from_json(data): pass
    @classmethod
    @abc.abstractmethod
    def from_model(model:InstalModelResult): pass
