##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from collections import defaultdict

from instal.interfaces.reporter import InstalReporter_i
from instal.defaults import STATE_HOLDSAT_GROUPS, TEX_loc
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- imports
from importlib.resources import files
##-- end imports

##-- data
data_path       = files("instal.__data.tex")
tex_path        = files(TEX_loc)

HEADER_PAT      = Template((data_path / "header_pattern").read_text())
PDF_PRELUDE_PAT = Template((tex_path / "pdf_prelude.tex").read_text())
##-- end data

class InstalPDFReporter(InstalReporter_i):
    """
        InstalPDFTracer
        Implementation of ABC InstalTracer for pdf output.
    """

    def other():
        observed = {t - 1: trace.states[t].observed for t in range(1, len(trace.trace))}

        occurred = defaultdict(list)
        for t in range(1, len(trace.states)):
            # 20170328 JAP: added sorting
            occurred[t - 1] = sorted(trace.states[t].occurred,
                                     key=lambda x: x.arguments[0].name)
        holdsat = defaultdict(list)
        for t in range(0, len(trace.states)):
            # 20170328 JAP: added filtering and sorting here and removed from later
            if remove_permpows:
                holdsat[t] = sorted((f for f in trace.states[t].holdsat
                                     if not (f.arguments[0].name in STATE_HOLDSAT_GROUPS)),
                                    key=lambda x: x.arguments[0].name)
            else:
                holdsat[t] = sorted(trace.states[t].holdsat,
                                key=lambda x: x.arguments[0].name)

        labels = {}
        states = {}
        tableWidth = "5cm"
        selected_states, selected_events = (
            set(range(0, len(observed) + 1)), set(range(0, len(observed))))

    def trace_to_file(self, trace, path):
        self.clear()
        self.insert(PDF_PRELUDE_PAT)

        # Event Macros
        # State Macros
        # Trace
        # State chain args
        # State chain nodes
        # State chain bodies
        # Event chain bodies
        # End Trace
        # End Document

        # write
        with open(path, 'w') as f:
            f.write("\n".join(self._compiled_text))
