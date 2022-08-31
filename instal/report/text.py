
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

    def trace_to_file(self, trace, path):
        with open(path, 'w') as f:
            f.write(str(trace))
