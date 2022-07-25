#/usr/bin/env python3
"""

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

from isntal.interfaces.ast import InstalAST

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


logging = logmod.getLogger(__name__)

class InstalChecker(metaclass=abc.ABCMeta):

    EXPR_SYMBOLS = ['==', '!=', '<', '>', '<=', '>=']

    def __init__(self, ir:InstalAST):
        self.IR = ir
        self.declaration_keys = None

    @abc.abstractmethod
    def check(self): pass

    def check_overloaded_arguments(self, final_types):
        for k, v in final_types.items():
            if len(v) > 1:
                raise InstalParserArgumentError(
                    "Overloaded variable {}".format(k))

    def get_types_dict(self, lhs_dict, rhs_dict, cond_dict):
        final_types = lhs_dict.copy()
        final_types = self.combine_defaultdicts(final_types, rhs_dict)
        final_types = self.combine_defaultdicts(final_types, cond_dict)
        return final_types

    def check_conditional_expr(self, final_types, condition):
        self.check_cond_expr(final_types, condition)

    def check_cond_expr(self, final_types, c):
        if len(c) < 2:
            return
        if c[0] == "and":
            self.check_cond_expr(final_types, c[1])
            self.check_cond_expr(final_types, c[2])
        elif c[0] == "not":
            self.check_cond_expr(final_types, c[1])
        elif c[0] in self.EXPR_SYMBOLS:
            type_1 = final_types.get(c[1][0], None)
            type_2 = final_types.get(c[1][1], None)
            if not type_1:
                raise InstalParserTypeError(
                    "{} in conditional but not bound.".format(c[1][0]))
            if not type_2:
                raise InstalParserTypeError(
                    "{} in conditional but not bound.".format(c[1][1]))
            if type_1 != type_2:
                raise InstalParserTypeError(
                    "Can't have an expression between {} ({}) and {} ({}) - mismatched types.".format(c[1][0], type_1, c[1][1], type_2))
        return

    def combine_defaultdicts(self, a, b):
        new = defaultdict(set)
        for k, v in chain(a.items(), b.items()):
            new[k].update(v)
        return new
