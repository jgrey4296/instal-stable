#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from importlib.resources import files
from re import Pattern
from string import Template
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

from instal.compiler.util import CompileUtil
from instal.errors import InstalCompileError
from instal.interfaces import ast as IAST
from instal.interfaces.compiler import InstalCompiler

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- resources
data_path   = files("instal.__data")
inst_data   = data_path / "institution"
bridge_data = data_path / "bridge"

HEADER         = Template((data_path   / "header_pattern").read_text())
INITIAL_FACT   = Template((inst_data   / "initial_fact_pattern.lp").read_text())

##-- end resources

class InstalSituationCompiler(InstalCompiler):
    def compile(self, facts:IAST.FactTotalityAST, inst:None|IAST.InstitutionDefAST=None, header=False):
        assert(all(isinstance(x, IAST.InitiallyAST) for x in facts.body))

        if header:
            self.insert(HEADER, header="Initial Situation Specification",
                        sub=facts.source if facts.source is not None else "")

        for initial in facts.body:
            for state in initial.body:
                if inst:
                    conditions  = CompileUtil.compile_conditions(inst, initial.conditions)
                    type_guards = CompileUtil.wrap_types(inst.types, state)
                    rhs = f"{conditions}, {type_guards}"
                    self.insert(INITIAL_FACT,
                                state=CompileUtil.compile_term(state),
                                inst=inst.head,
                                rhs=rhs)
                else:
                    assert(initial.inst is not None)
                    assert(not bool(initial.conditions))
                    inst_term  = CompileUtil.compile_term(initial.inst)
                    state_term = CompileUtil.compile_term(state)
                    rhs        = CompileUtil.wrap_types(None, state)
                    self.insert(INITIAL_FACT,
                                state=state_term,
                                inst=inst_term,
                                rhs=rhs)

        return "\n".join(self._compiled_text)
