#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import warnings
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

from instal.interfaces.ast import InstalAST

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


logging = logmod.getLogger(__name__)

class InstalChecker_i(metaclass=abc.ABCMeta):


    def warn(self, msg):
        warnings.warn(msg)

    def error(self, msg):
        raise Exception(msg)

    @abc.abstractmethod
    def check(self, ast:iast.InstalAST): pass
