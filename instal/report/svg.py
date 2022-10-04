##-- imports
from __future__ import annotations

import logging as logmod
import sys

from instal.interfaces.reporter import InstalReporter_i
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class InstalSVGReporter(InstalReporter_i):
    """
    Exports a Trace as an html svg image
    """

    def trace_to_file(self, trace, path):
        with open(path, 'w') as f:
            f.write(str(trace))
