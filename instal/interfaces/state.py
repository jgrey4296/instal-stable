#/usr/bin/env python3
"""

"""
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

if TYPE_CHECKING:
    # tc only imports
    pass

logging = logmod.getLogger(__name__)


class State_Protocol(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    @staticmethod
    def from_json(path): pass

    @abc.abstractmethod
    @staticmethod
    def from_symbol_list(lst): pass

    @abc.abstractmethod
    def to_json(self): pass

    @abc.abstractmethod
    def to_list(self): pass

    @abc.abstractmethod
    def __str__(self): pass

    @abc.abstractmethod:
    def to_ir(self): pass

    @abc.abstractmethod:
    def to_solver(self): pass



    @abc.abstractmethod
    def check(self, conditions): pass

@dataclass
class State(InstalState_Protocol):

    metadata : dict         = field(default_factory=dict)
    holdsat  : list[Symbol] = field(default_factory=list)
    occurred : list[Symbol] = field(default_factory=list)
    observed : list[Symbol] = field(default_factory=list)



class Trace(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    @classmethod
    def from_json(data): pass

    @abc.abstractmethod
    @classmethod
    def from_list(lst): pass

    @abc.abstractmethod
    def append(self, data): pass

    @abc.abstractmethod
    def to_json(self): pass

    @abc.abstractmethod
    def __str__(self): pass

    @abc.abstractmethod
    def check(self, conditions): pass

    @abc.abstractmethod
    def __contains__(self, conditions): pass

    @abc.abstractmethod
    def last(self): pass