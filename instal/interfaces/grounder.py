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

class Grounder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def ground_files(self, file_group:InstalFileGroup) -> defaultdict(set): pass
