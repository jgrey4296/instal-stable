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
from instal.interfaces.compiler import InstalCompiler_i
from instal.defaults import COMP_DATA_loc

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- resources
data_path   = files(COMP_DATA_loc)

HEADER         = Template((data_path / "header_pattern").read_text())
INITIAL_FACT   = Template((data_path / "initial_fact_pattern.lp").read_text())
PROGRAM_PAT    = Template((data_path / "program_pattern.lp").read_text())
##-- end resources

class InstalSituationCompiler(InstalCompiler_i):
    def compile(self, facts:list[IAST.InitiallyAST], inst:None|IAST.InstitutionDefAST=None, header=False):
        assert(all(isinstance(x, IAST.InitiallyAST) for x in facts))

        if header:
            self.insert(HEADER, header="Initial Situation Specification",
                        sub=facts[0].sources_str)

        self.insert(PROGRAM_PAT, prog="base")
        for initial in facts:
            for state in initial.body:
                if inst:
                    inst_head   = CompileUtil.compile_term(inst.head)
                    state_term  = CompileUtil.compile_term(state)
                    conditions  = CompileUtil.compile_conditions(inst, initial.conditions)
                    type_guards = CompileUtil.wrap_types(inst.types, state)
                    rhs         = ", ".join(sorted(conditions | type_guards))
                    self.insert(INITIAL_FACT,
                                state=state_term,
                                inst=inst_head,
                                rhs=rhs)
                else:
                    assert(initial.inst is not None)
                    assert(not bool(initial.conditions))
                    assert(not any(y.has_var for x in facts for y in x.body))
                    inst_term  = CompileUtil.compile_term(initial.inst)
                    state_term = CompileUtil.compile_term(state)
                    rhs        = "true"
                    self.insert(INITIAL_FACT,
                                state=state_term,
                                inst=inst_term,
                                rhs=rhs)

        return self.compilation
