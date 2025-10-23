#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from collections import deque
from enum import Enum, auto
import re
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import instal.interfaces.ast as ASTs
from instal.defaults import DEONTICS, BRIDGE_DEONTICS

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

type_matcher = re.compile(r"([A-Z][^0-9_]*)(?:_?([0-9]+))?")

class _TermCompileEnum:
    START_PARAM = auto()
    STOP_PARAM  = auto()
    COMMA = auto()


class CompileUtil:
    @staticmethod
    def wrap_types(types:list[ASTs.DomainSpecAST], *params:ASTs.TermAST) -> set[str]:
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
        result                = set(["true"])
        type_check : set[str] = {x.head.value.lower() for x in types} if bool(types) else set()
        queue                 = list(params)
        found                 = set()
        while bool(queue):
            param = queue.pop()
            if param is None:
                continue
            if not param.is_var:
                queue += param.params
                continue

            matcher    = type_matcher.match(param.value)
            assert(matcher is not None), param.value
            type_name  = matcher[1].lower()
            # var_num    = matcher[2] if matcher[2] else ""
            # var_name   = matcher[1] + var_num
            var_name = param.value
            if var_name in found:
                continue

            assert(not bool(param.params))
            # assert(not bool(type_check) or type_name in type_check), param

            result.add(f"{type_name}({var_name})")
            found.add(var_name)

        return result

    @staticmethod
    def compile_conditions(inst, all_conditions:list[ASTs.ConditionAST]) -> set[str]:
        # TODO handle condiitons that are events
        assert(all(isinstance(x, ASTs.ConditionAST) for x in all_conditions))

        result          = set(["true"])
        inst_head : str = CompileUtil.compile_term(inst.head)
        for condition in all_conditions:
            term = CompileUtil.compile_term(condition.head)
            result |= CompileUtil.wrap_types(inst.types, condition.head, condition.rhs)
            match condition.operator, condition.rhs:
                case None, None if condition.negated:
                    result.add(f"not holdsat({term}, {inst_head}, I)")
                case None, None:
                    result.add(f"holdsat({term}, {inst_head}, I)")
                case str(), ASTs.TermAST():
                    rhs_term = CompileUtil.compile_term(condition.rhs)
                    result.add(f"{term}{condition.operator}{rhs_term}")
                case _:
                    raise TypeError("Confusing condition found: ", condition)

        return result


    @staticmethod
    def compile_term_recursive(term, top=True) -> str:
        term_name = term.value
        params = ""
        match term_name, term.params:
            case x, [*values] if x in DEONTICS:
                term_name = "deontic"
                params     = "({})".format(", ".join([x] + [CompileUtil.compile_term_recursive(y, top=False) for y in values]))
            case x, [*values] if x in BRIDGE_DEONTICS:
                term_name = "deontic"
                params     = "({}, ev({}))".format(x, ", ".join([CompileUtil.compile_term_recursive(y, top=False) for y in values]))
            case _, []:
                params = ""
            case _, [*values]:
                params = "({})".format(", ".join([CompileUtil.compile_term_recursive(x, top=False) for x in values]))

        return f"{term_name}{params}"

    @staticmethod
    def compile_term(term) -> str:
        result = []
        queue  = deque([term])
        param_clause_count = 0
        while bool(queue):
            current = queue.popleft()
            match current:
                case str():
                    result.append(current)
                case _TermCompileEnum.START_PARAM:
                    result.append('(')
                    param_clause_count += 1
                case _TermCompileEnum.STOP_PARAM:
                    result.append(')')
                    param_clause_count -= 1
                case ASTs.TermAST(value=x, params=[]) if x in DEONTICS or x in BRIDGE_DEONTICS:
                    raise Exception("Deontics should wrap something", current)
                case ASTs.TermAST(value=x, params=[*params]) if x in DEONTICS:
                    # convert power(something) to deontic(power, something)
                    result.append("deontic")
                    new_form = ([_TermCompileEnum.START_PARAM, x]
                                + params
                                + [_TermCompileEnum.STOP_PARAM])
                    queue.extendleft(reversed(new_form))
                case ASTs.TermAST(value=x, params=[*params]) if x in BRIDGE_DEONTICS:
                    # convert initPower(src, act, sink) to deontic(initPower, ev(src, act, sink))
                    result.append("deontic")
                    new_form = ([_TermCompileEnum.START_PARAM, x, "ev", _TermCompileEnum.START_PARAM]
                                + params
                                + [_TermCompileEnum.STOP_PARAM, _TermCompileEnum.STOP_PARAM])
                    queue.extendleft(reversed(new_form))
                case ASTs.TermAST(value=x, params=[]):
                    result.append(x)
                case ASTs.TermAST(value=x, params=[*params]):
                    result.append(x)
                    new_form = ([_TermCompileEnum.START_PARAM]
                                + params
                                + [_TermCompileEnum.STOP_PARAM])
                    queue.extendleft(reversed(new_form))

            if (bool(queue)
                and bool(result)
                and result[-1] != "("
                and queue[0] not in {_TermCompileEnum.START_PARAM, _TermCompileEnum.STOP_PARAM}
                and param_clause_count > 0):
                result.append(", ")

        return "".join(result)
