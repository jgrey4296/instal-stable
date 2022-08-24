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
from clingo import Symbol
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.state import State, Trace
from instal.state.instal_ast_state import InstalASTState

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalTrace(Trace):
    """ A Workable representation of a sequence of Instal Model time steps.
    Each time step is an `InstalState`

    """
    state_class : ClassVar[State] = InstalASTState

    def __init__(self, states=None, filename=None):
        self.states   = states or []
        self.filename = filename

    @classmethod
    def from_json(cls, json : List[Dict],filename : str = None) -> "InstalStateTrace":
        trace = InstalStateTrace()
        trace.filename = filename
        for d in json:
            trace.append_from_json(d)
        return trace

    @classmethod
    def from_model(cls, model:InstalModelResult, model_length:int=1, metadata:dict=None) -> "InstalStateTrace":
        metadata = metadata or {}
        states = [cls.state_class(i, metadata.copy()) for i in range(model_length)]
        for term in model.shown:
            # Get the step
            assert(isinstance(term.arguments[-1], int))
            assert(term.arguments[-1] < len(states))
            state = states[term.arguments[-1]]
            # Insert it
            state.append(term)

        trace = InstalStateTrace()
        for state in states:
            trace.states.append(state)

        return trace


    def to_json(self) -> List[Dict]:
        return [s.to_json() for s in self.trace]

    def __str__(self, show_perms=True, show_pows=True, show_cross=True) -> str:
        # Should string out contain some annotations? Maybe prefixed with % ?
        string_out = ""
        last = self.trace[-1]
        string_out += "% Answer Set {} of {}. (Cost: {})\n".format(last.metadata.get("answer_set_n"),last.metadata.get("answer_set_of"),last.metadata.get("cost",0))
        timestep = 1
        for s in self.trace[1:]:
            string_out += "\n% Timestep {}.\n".format(timestep)
            string_out += s.to_str(show_perms=show_perms, show_pows=show_pows, show_cross=show_cross)
            timestep += 1
        return string_out

    def __contains__(self, conditions) -> int:
        # Used for test cases.
        pass

    def last(self) -> InstalState:
        return self.trace[-1]

    def check(self, conditions:list, verbose:int=2) -> int:
        """A wrapper for check_trace_for that checks if the length of the trace and conditions are the same.
        """
        errors = 0
        if len(self.trace) == len(conditions):
            offset = 0
        elif len(self.trace) == len(conditions) + 1:
            offset = 1
        else:
            raise Exception("Trace given not long enough. (Trace: {}, conditions: {})".format(
                len(self.trace), len(conditions)))
        for i in range(0, len(conditions)):
            errors += self.trace[i + offset].check_trace_for(conditions[i], verbose)
        return errors
