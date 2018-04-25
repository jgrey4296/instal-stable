from abc import ABCMeta

from instal.state.InstalStateTrace import InstalStateTrace


class InstalTracer(metaclass=ABCMeta):
    """
        InstalTracer
        See __init__.py for more details.
    """

    def __init__(self, trace: InstalStateTrace, output_file_name: str, zeroth_term: bool=False):
        self.trace = trace
        self.zeroth_term = zeroth_term
        self.output_file_name = output_file_name
        self.check_trace()

    def check_trace(self):
        pass

    def trace_to_file(self) -> None:
        raise NotImplementedError
