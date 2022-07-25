##-- imports
import abc
from dataclasses import InitVar, dataclass, field

from instal.state.InstalStateTrace import InstalStateTrace
##-- end imports

@dataclass
class Reporter(metaclass=abc.ABCMeta):
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
