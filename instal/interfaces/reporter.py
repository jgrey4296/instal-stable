##-- imports
from __future__ import annotations

import abc
from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)

from instal.interfaces.state import Trace

##-- end imports

@dataclass
class InstalReporter(metaclass=abc.ABCMeta):
    """
        InstalTracer
        See __init__.py for more details.
    """
    trace            : Any = field()
    zeroth_term      : Any = field()
    output_file_name : str = field()

    def __post_init__(self):
        self.check_trace()

    @abc.abstractmethod
    def check_trace(self): pass

    @abc.abstractmethod
    def trace_to_file(self): pass
