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

import instal.interfaces.ast as iAST
import simplejson as json
from clingo import Symbol, SymbolType
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.trace import State_i, Trace_i
from instal.trace.ast_state import InstalASTState

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalTrace(Trace_i):
    """ A Workable representation of a sequence of Instal Model time steps.
    Each time step is an `InstalState`

    """
    state_constructor: ClassVar[State_i] = InstalASTState

    @staticmethod
    def from_json(json : List[Dict],filename : str = None) -> "InstalStateTrace":
        trace = InstalStateTrace()
        trace.filename = filename
        for d in json:
            trace.append_from_json(d)
        return trace

    @staticmethod
    def from_model(model:InstalModelResult, steps:int=1, metadata:dict=None) -> "InstalStateTrace":
        metadata                   = metadata or {}
        metadata['cost']           = model.cost
        metadata['current_result'] = model.number
        metadata['optimal']        = model.optimal

        states   = [InstalTrace.state_constructor(i)
                    for i in range(steps + 1)]
        for term in model.shown:
            # Get the step
            match term.arguments[-1]:
                case int() as x if x < len(state):
                    state = states[x]
                case Symbol() as x if x.type == SymbolType.Number and x.number < len(states):
                    state = states[x.number]
                case _:
                    raise Exception("Unexpected Term in Trace", term)

            # add to appropriate state
            state.insert(term)

        # Wrap as a trace
        trace = InstalTrace(states, metadata=metadata)
        return trace



    def __repr__(self) -> str:
        result = []
        result.append(f"----- Instal Trace {self.metadata['current_result']} of {self.metadata['result_size']}.")
        result.append(f"Cost  : {self.metadata['cost']}")
        result.append(f"Length: {len(self.states)}")
        result.append("")
        for state in self[:]:
            result.append(str(state))

        return "\n".join(result)

    def __contains__(self, conditions) -> int:
        # Used for test cases.
        pass

    def to_json(self) -> List[Dict]:
        return [s.to_json() for s in self.trace]


    def meets(self, conditions:list) -> bool:
        pass
    def check(self, conditions:list) -> bool:
        """
        A wrapper for check_trace_for that checks if the length of the trace and conditions are the same.
        """
        errors = 0
        if len(self.trace) == len(conditions):
            offset = 0
        elif len(self.trace) == len(conditions) + 1:
            offset = 1
        else:
            raise Exception("Trace_i given not long enough. (Trace_i: {}, conditions: {})".format(
                len(self.trace), len(conditions)))
        for i in range(0, len(conditions)):
            errors += self.trace[i + offset].check_trace_for(conditions[i], verbose)
        return bool(errors)
