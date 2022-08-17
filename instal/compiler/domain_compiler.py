#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
from string import Template
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from importlib.resources import files
from re import Pattern
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

class InstalDomainCompiler(InstalCompiler):
    def compile(self, domain:IAST.DomainTotalityAST) -> str:
        """
        Compile idc domain specs of Type: instance, instance, instance...
        """
        assert(all(isinstance(x, IAST.DomainSpecAST) for x in domain.body))
        self.clear()
        self.insert(HEADER, header="Domain Specification",
                    sub=domain.source if domain.source is not None else "")
        for assignment in domain.body:
            wrapper = assignment.head.value.lower()
            for term in assignment.body:
                assert(not bool(term.params))
                term_str = CompileUtil.compile_term(term)
                self.insert(f"{wrapper}({term_str}).")

        return "\n".join(self._compiled_text)
