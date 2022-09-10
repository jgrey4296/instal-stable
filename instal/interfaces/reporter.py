##-- imports
from __future__ import annotations

import abc
from pathlib import Path
from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)

from instal.interfaces.trace import Trace_i
from string import Template
##-- end imports

@dataclass
class InstalReporter_i(metaclass=abc.ABCMeta):
    """
        InstalTracer
        See __init__.py for more details.
    """

    def __init__(self):
        self._compiled_text : list[str] = []

    def clear(self):
        self._compiled_text = []

    def expand(self, pattern:str|Template, **kwargs):
        match pattern:
            case Template():
                return pattern.safe_substitute(kwargs)
            case str() if not bool(kwargs):
                return pattern
            case str():
                return pattern.format_map(kwargs)
            case _:
                raise TypeError("Unrecognised compile pattern type", pattern)

    def insert(self, pattern:str|Template, **kwargs):
        """
        insert a given pattern text into the compiled output,
        formatting it with kwargs.
        """
        self._compiled_text.append(self.expand(pattern, **kwargs))

    @abc.abstractmethod
    def trace_to_file(self, trace:Trace_i, path:Path): pass
