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

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class CompileUtil:
    @staticmethod
    def wrap_types(types:list[IAST.TypeAST], *params:IAST.TermAST) -> str:
        """
        convert instal variables (User, Book etc)
        to terms for the right hand side of rules to ensure correct typing:
        user(User), book(Book) etc.
        """
        type_check : set[str] = {x.head for x in types} if bool(types) else set()
        result                = []
        queue                 = list(params)
        found                 = set()
        while bool(queue):
            param = queue.pop()
            if str(param) in found:
                continue
            if not param.is_var:
                queue += param.params
                continue
            assert(not bool(param.params))
            assert(param.value[0].isupper())
            assert(not bool(type_check) or param.value in type_check)
            # TODO handle variable numbers
            result.append(f"{param.value.lower()}({param.value})")
            found.add(param)

        if bool(result):
            return ", ".join(result)
        else:
            return "true"


    @staticmethod
    def compile_conditions(inst, all_conditions) -> str:
        if not bool(conds):
            return "true"

        results = []
        for condition in all_conditions:
            cond : list[str] = []
            if condition.negated:
                cond.append("not ")

            if condition.operator is None and condition.rhs is None:
                term = CompileUtil.compile_term(condition.head)
                results.append(CompileUtil.wrap_types(inst.types, condition.head))
                cond.append(f"holdsat({term}, {inst.head}, I)")
            else:
                assert(condition.operator is not None and condition.rhs is not None)
                results.append(CompileUtil.wrap_types(inst.types, condition.head, condition.rhs))
                cond.append(CompileUtil.compile_term(condition.head))
                cond.append(condtion.operator)
                cond.append(CompileUtil.compile_term(condition.rhs))

            results.append("".join(cond))


        return ", ".join(results)


    @staticmethod
    def compile_term(term) -> str:
        match term.params:
            case []:
                params = ""
            case [*values]:
                params = "({})".format(", ".join([CompileUtil.compile_term(x) for x in term.params]))
        return f"{term.value}{params}"

