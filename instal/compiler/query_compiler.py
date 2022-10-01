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
from instal.defaults import INSTITUTION_DATA_loc, BRIDGE_DATA_loc, DATA_loc

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- resources
data_path   = files(DATA_loc)
inst_data   = files(INSTITUTION_DATA_loc)
bridge_data = files(BRIDGE_DATA_loc)

HEADER         = Template((data_path / "header_pattern").read_text())
QUERY_PAT      = Template((inst_data / "query_pattern.lp").read_text())
PROGRAM_PAT    = Template((inst_data / "program_pattern.lp").read_text())
##-- end resources

class InstalQueryCompiler(InstalCompiler_i):
    def compile(self, query:list[IAST.QueryAST]) -> str:
        """
        Compile sequence of observations into extObserved facts
        # TODO handle specifying time of observation
        """
        assert(all(isinstance(x, IAST.QueryAST) for x in query))
        self.clear()
        self.insert(HEADER, header="Query Specification",
                    sub=query[0].sources_str)
        self.insert(PROGRAM_PAT, prog="base")
        for i, q in enumerate(query):
            if q.time is not None:
                i = q.time
            term_str = CompileUtil.compile_term(q.head)
            self.insert(QUERY_PAT,
                        term=term_str,
                        i=i)

        return self.compilation
