import sys

from .InstalTracer import InstalTracer


class InstalTextTracer(InstalTracer):
    """
        InstalTextTracer
        Implementation of ABC InstalTracer for text output.
        Will produce same output as instalsolve's verbose=1 option.
    """

    def trace_to_file(self):
        f = None
        if self.output_file_name == "-":
            f = sys.stdout
        with open(self.output_file_name, 'w') if not f else f as tfile:
            print(self.trace.to_str(), file=tfile)
