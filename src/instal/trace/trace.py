#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import sys
import abc
import json
from collections import defaultdict
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
        metadata  = json['metadata']
        trace_len = metadata['model_length']

        states   = [InstalTrace.state_constructor(i)
                    for i in range(trace_len + 1)]
        for state_dict in json['states']:
            assert(isinstance(state_dict, dict))
            step = state_dict['timestep']
            state = states[step]
            for k,v in state_dict.items():
                if k == "timestep":
                    continue
                if k == "holdsat" and isinstance(v, dict):
                    terms = [y for x in v.values() for y in x]
                else:
                    terms = v

                for term in terms:
                    state.insert(term)

        # Wrap as a trace
        trace = InstalTrace(states, metadata=metadata)
        return trace

    @staticmethod
    def from_model(model:InstalModelResult, steps:int=1, sources:list[str]=None, metadata:dict=None) -> "InstalStateTrace":
        """
        Given a model, construct a trace
        """
        metadata                   = metadata or {}
        metadata['cost']           = model.cost
        metadata['current_result'] = model.number
        metadata['optimal']        = model.optimal
        metadata['model_length']   = steps
        metadata['instal_files']   = [str(x) for x in sources or []]
        metadata['institutions']  = []

        i_set : set[str] = set()
        states   = [InstalTrace.state_constructor(i)
                    for i in range(steps + 1)]
        for term in model.shown:
            if term.name == "institution":
                i_set.add(str(term.arguments[0]))
                continue

            # Get the step
            match term.arguments[-1]:
                case int() as x if x < len(state):
                    state = states[x]
                case Symbol() as x if x.type == SymbolType.Number and x.number < len(states):
                    state = states[x.number]
                case str() as x if int(x) < len(state):
                    state = states[int(x)]
                case _:
                    raise Exception("Unexpected Term in Trace", term)

            # add to appropriate state
            state.insert(term)

        # Wrap as a trace
        metadata['institutions'] += list(i_set)
        trace = InstalTrace(states, metadata=metadata)
        return trace

    def __repr__(self) -> str:
        result = []
        result.append(f"----- Instal Trace {self.metadata['current_result']} of {self.metadata['result_size']}.")
        result.append(f"Cost  : {self.metadata['cost']}")
        result.append(f"Length: {self.metadata['model_length']}")
        result.append("")
        for state in self:
            result.append(str(state))

        return "\n".join(result)

    def __contains__(self, conditions) -> int:
        # Used for test cases.
        pass

    def to_json_str(self, filename=None) -> str:
        trace_obj = {
            "metadata" : self.metadata,
            "states"   : [s.to_json() for s in self]
            }
        if filename is not None:
            trace_obj['metadata']['filename'] = str(filename)

        return json.dumps(trace_obj, sort_keys=True, indent=4)

    def check(self, conditions:list) -> bool:
        pass

    def filter(self, allow:list[str], reject:list[str], start:None|int=None, end:None|int=None) -> Trace_i:
        logging.info("Filtering")
        start           = start or 0
        end             = end if (end is not None) else -1
        end_proper      = end if end > -1 else sys.maxsize

        in_range        = [x for x in self if x.timestep >= start and x.timestep <= end_proper]
        filtered_states = [x.filter(allow, reject) for x in in_range] if allow or reject else in_range

        filtered_trace  = InstalTrace(filtered_states, metadata=self.metadata.copy())

        return filtered_trace

    def fluent_intervals(self) -> list[tuple[str, int, int]]:
        """
        Convert the Trace's individual timesteps
        into a set of intervals for each fluent.
        [fluent: TermAST, stepOn:int, stepOff:int]
        """
        results  = []
        # dict to track when a fluent enters and exits
        tracking : dict[str, list] = {}

        for state in self:
            curr_time = state.timestep
            for fluent in state.fluents:
                key = str(fluent.params[0])
                match key in tracking:
                    case False:
                        tracking[key] = [fluent, curr_time, curr_time]
                    case True:
                        tracking[key][-1] = curr_time

        return list(tracking.values())
