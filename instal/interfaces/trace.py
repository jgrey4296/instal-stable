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
from instal.defaults import STATE_HOLDSAT_GROUPS
from clingo import Symbol

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


logging = logmod.getLogger(__name__)


@dataclass
class State_i:
    """
    Description of a single moment in a model's trace.
    """

    timestep : int            = field(default=0)
    holdsat  : dict[str, Any] = field(default_factory=dict)
    occurred : list[Any]      = field(default_factory=list)
    observed : list[Any]      = field(default_factory=list)
    rest     : list[Any]      = field(default_factory=list)

    def __post_init__(self):
        for x in STATE_HOLDSAT_GROUPS:
            self.holdsat[x] = []

    @property
    def fluents(self) -> iter[Any]:
        """ Iterate through all the fluents as a list
        instead of as a dict of separate types of fluent
        """
        for items in self.holdsat.values():
            for entry in items:
                yield entry


    @abc.abstractmethod
    def __repr__(self): pass

    @abc.abstractmethod
    def to_json(self) -> dict: pass

    @abc.abstractmethod
    def check(self, conditions) -> bool: pass

    @abc.abstractmethod
    def insert(self, val:str|TermAST|Symbol): pass


    @abc.abstractmethod
    def filter(self, allow:list[Any], reject:list[Any]) -> State_i: pass

@dataclass
class Trace_i(Sequence):
    """
    The collected sequence of instance states which comprise
    a full model run
    """
    states   : list[State_i] = field(default_factory=list)
    metadata : dict          = field(default_factory=dict)

    state_constructor : ClassVar[State_i] = None

    @staticmethod
    @abc.abstractmethod
    def from_json(data): pass
    @staticmethod
    @abc.abstractmethod
    def from_model(model:InstalModelResult, steps:int=1): pass
    def __getitem__(self, index):
        return self.states[index]

    def __iter__(self):
        return iter(self.states)

    def contextual_iter(self) -> iter[tuple]:
        """
        provide an iterator of tuples
        [timestep, state, state-1, state+1]
        """
        return zip(range(len(self)),
                   self.states,
                   [None] + self.states,
                   self.states[1:] + [None])

    def __len__(self):
        return len(self.states)

    def last(self) -> State_i:
        return self.trace[-1]

    @abc.abstractmethod
    def __repr__(self): pass

    @abc.abstractmethod
    def meets(self, conditions:list) -> bool: pass
    @abc.abstractmethod
    def check(self, conditions:list) -> bool: pass
    @abc.abstractmethod
    def to_json(self) -> dict: pass


    @abc.abstractmethod
    def filter(self, allow:list[Any], reject:list[Any], start=None, end=None) -> Trace_i: pass