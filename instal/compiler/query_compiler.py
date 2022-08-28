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
INST_PRELUDE   = Template((inst_data   / "institution_prelude.lp").read_text())
BRIDGE_PRELUDE = Template((bridge_data / "bridge_prelude.lp").read_text())

TYPE_PAT       = Template((inst_data   / "type_def_guard.lp").read_text())
TYPE_GROUND    = Template((inst_data   / "type_ground_pattern.lp").read_text())

INITIAL_FACT   = Template((inst_data   / "initial_fact_pattern.lp").read_text())

EXO_EV         = Template((inst_data   / "exogenous_event_pattern.lp").read_text())
INST_EV        = Template((inst_data   / "inst_event_pattern.lp").read_text())
VIOLATION_EV   = Template((inst_data   / "violation_event_pattern.lp").read_text())
NULL_EV        = Template((inst_data   / "null_event_pattern.lp").read_text())

IN_FLUENT      = Template((inst_data   / "inertial_fluent_pattern.lp").read_text())
NONIN_FLUENT   = Template((inst_data   / "noninertial_fluent_pattern.lp").read_text())
OB_FLUENT      = Template((inst_data   / "obligation_fluent_pattern.lp").read_text())

CROSS_FLUENT   = Template((bridge_data / "cross_fluent.lp").read_text())
GPOW_FLUENT    = Template((bridge_data / "gpow_cross_fluent.lp").read_text())

GEN_PAT        = Template((inst_data   / "generate_rule_pattern.lp").read_text())
INIT_PAT       = Template((inst_data   / "initiate_rule_pattern.lp").read_text())
TERM_PAT       = Template((inst_data   / "terminate_rule_pattern.lp").read_text())

X_GEN_PAT      = Template((bridge_data / "xgenerate_rule_pattern.lp").read_text())
X_INIT_PAT     = Template((bridge_data / "xinitiate_rule_pattern.lp").read_text())
X_TERM_PAT     = Template((bridge_data / "xterminate_rule_pattern.lp").read_text())

NIF_RULE_PAT   = Template((inst_data   / "nif_rule_pattern.lp").read_text())

##-- end resources

class InstalQueryCompiler(InstalCompiler_i):
    def compile(self, query:IAST.QueryTotalityAST) -> str:
        """
        Compile sequence of observations into extObserved facts
        # TODO handle specifying time of observation
        """
        assert(all(isinstance(x, IAST.QueryAST) for x in query.body))
        self.clear()
        self.insert(HEADER, header="Query Specification",
                    sub=query.parse_source if query.parse_source is not None else "")
        for i, q in enumerate(query.body):
            if q.time is not None:
                i = q.time
            term_str = CompileUtil.compile_term(q.head)
            self.insert(f"extObserved({term_str}, {i}).")
            self.insert(f"_eventSet({i}).")

        return "\n".join(self._compiled_text)
