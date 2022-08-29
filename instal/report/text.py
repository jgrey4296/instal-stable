
##-- imports
from __future__ import annotations

import logging as logmod
import sys

from instal.interfaces.reporter import InstalReporter_i
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class InstalTextReporter(InstalReporter_i):
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
