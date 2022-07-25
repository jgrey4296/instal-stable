#/usr/bin/env python3
"""
helper class to compile clingo rules
allowing appending to a list, which automatically
adds commas and a final full stop, indents, etc
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
from dataclasses import dataclass, field, InitVar

from clingo import ast
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class ClingoRuleWriter:

    head     : None|str       = field(default=None)
    params   : list[str] = field(default_factory=list)
    body     : list[str] = field(default_factory=list)
    comments : list[str] = field(default_factory=list)

    def append(self, *terms):
        """
        insert terms into the rule's body
        """
        self.body += terms

    def write(self) -> str:
        """
        Compile the rule into a string consumable by clingo
        """
        pass

    def __len__(self):
        return len(self.body)

    @property
    def integrity_constraint(self) -> bool:
        return self.head is None

    @property
    def fact(self) -> bool:
        return not bool(self.body)

    def _build_var(self, name):
        pass

    def _build_id(self, name):
        pass

    def _build_function(self, name, args):
        pass

    def _build_comparison(self, op, left, right):
        pass

