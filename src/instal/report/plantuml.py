#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations
import logging as logmod
from instal.interfaces.reporter import InstalReporter_i
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class InstalPlantUMLReporter(InstalReporter_i):
    """
        InstalPlantUMLReporter
        Implementation of ABC InstalTracer for plantuml visualisation.
    """

    def trace_to_file(self, trace, path):
        with open(path, 'w') as f:
            f.write(str(trace))
