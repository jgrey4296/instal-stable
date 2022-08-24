
##-- imports
from __future__ import annotations

import abc
import logging as logmod
import time
import warnings
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from typing import IO, List

from clingo import parse_term
##-- end imports

logging = logmod.getLogger(__name__)

@dataclass
class InstalModelResult:
    """
    The immediate results data structure returned by a solver.
    Does no translation from the data structures the solver uses.

    ie: for Clingo, it is lists of clingo.Symbol's
    """
    atoms   : list[Any]
    shown   : list[Any]
    cost    : float
    number  : int
    optimal : bool
    type    : Any


class _SolverWrapper_Protocol(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def solve(self, events:None|list[Any]=None, situation:None|list[Any]=None, fresh=False) -> int: pass

    @property
    @abc.abstractmethod
    def metadata(self): pass

@dataclass
class SolverWrapper(_SolverWrapper_Protocol):
    """
    An wrapper around a solver (ie: clingo) to interface with the rest of instal
    """

    program        : None|str                = field(default=None)
    input_files    : list[Path]              = field(default_factory=list, kw_only=True)

    timestamp      : float                   = field(init=False, default_factory=time.time)
    results        : list[InstalModelResult] = field(init=False, default_factory=list)
    current_answer : int                     = field(init=False, default=0)
    cycle          : int                     = field(init=False, default=0)
    observations   : list[TermAST]           = field(default_factory=list)


    def __post_init__(self): pass
