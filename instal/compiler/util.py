#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
import re
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import instal.interfaces.ast as ASTs

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

type_matcher = re.compile(r"([A-Z][^0-9_]+)(?:_?([0-9]+))?")

class CompileUtil:
    @staticmethod
    def wrap_types(types:list[ASTs.TypeAST], *params:ASTs.TermAST) -> str:
        """
        convert instal variables (User, Book etc)
        to terms for the right hand side of rules to ensure correct typing:
        user(User), book(Book) etc.

        if there are no types to reify, just returns "true" : str.

        Handles multiple variables of the same type, numbered.
        So:
        similar(fantasy(Book_1), romance(Book_2))
        ->
        book(Book_1), book(Book_2).
        """
        type_check : set[str] = {x.head.value.lower() for x in types} if bool(types) else set()
        result                = []
        queue                 = list(params)
        found                 = set()
        while bool(queue):
            param = queue.pop()
            if not param.is_var:
                queue += param.params
                continue

            matcher   = type_matcher.match(param.value)
            type_name  = matcher[1].lower()
            var_num    = ("_" + matcher[2]) if matcher[2] else ""
            var_name   = matcher[1] + var_num
            if var_name in found:
                continue

            assert(not bool(param.params))
            assert(not bool(type_check) or type_name in type_check), param

            result.append(f"{type_name}({var_name})")
            found.add(var_name)

        if bool(result):
            return ", ".join(sorted(result))
        else:
            return "true"


    @staticmethod
    def compile_conditions(inst, all_conditions:list[ASTs.ConditionAST]) -> str:
        if not bool(all_conditions):
            return "true"

        assert(all(isinstance(x, ASTs.ConditionAST) for x in all_conditions))

        results = set()
        inst_head : str = CompileUtil.compile_term(inst.head)
        for condition in all_conditions:
            cond : list[str] = []
            if condition.operator is None and condition.rhs is None:
                if condition.negated:
                    cond.append("not ")

                results.add(CompileUtil.wrap_types(inst.types, condition.head))

                term = CompileUtil.compile_term(condition.head)
                cond.append(f"holdsat({term}, {inst_head}, I)")
            else:
                assert(condition.operator is not None and condition.rhs is not None)
                results.add(CompileUtil.wrap_types(inst.types, condition.head, condition.rhs))

                cond.append(CompileUtil.compile_term(condition.head))
                cond.append(condition.operator)
                cond.append(CompileUtil.compile_term(condition.rhs))

            # Filters out duplcated 'true's from wrap_types:
            results.add("".join(cond))


        return ", ".join(x for x in sorted(results) if x != "true")


    @staticmethod
    def compile_term(term) -> str:
        match term.params:
            case []:
                params = ""
            case [*values]:
                params = "({})".format(", ".join([CompileUtil.compile_term(x) for x in term.params]))
        return f"{term.value}{params}"

