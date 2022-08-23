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
##-- end resources

class InstalDomainCompiler(InstalCompiler):
    def compile(self, domain:IAST.DomainTotalityAST) -> str:
        """

        """
        assert(all(isinstance(x, IAST.DomainSpecAST) for x in domain.body))
        self.clear()
        self.insert(HEADER, header="Domain Specification",
                    sub=domain.parse_source if domain.parse_source is not None else "")
        for assignment in domain.body:
            wrapper = assignment.head.value.lower()
            for term in assignment.body:
                assert(not bool(term.params))
                term_str = CompileUtil.compile_term(term)
                self.insert(f"{wrapper}({term_str}).")

        return "\n".join(self._compiled_text)
