
##-- imports
from __future__ import annotations

import logging as logmod
from collections import defaultdict

from instal.interfaces.reporter import InstalReporter_i
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

def invert(d):
    result = defaultdict(list)
    for k in d:
        for v in d[k]:
            result[v] = result[v] + [k]
    return result

class InstalGanttReporter(InstalReporter_i):
    """
    InstalGanttTracer
    Implementation of ABC Reporter for gantt output.
    """

    def trace_to_file(self, remove_permpows=True):


        # TODO use __data.gant.gant_header.latex
        latex_gannt_header = None

        observed = {t: self.trace.trace[t].observed
                    for t in range(1, len(self.trace.trace))}
        occurred = defaultdict(list)
        for t in range(1, len(self.trace.trace)):
            occurred[t] = self.trace.trace[t].occurred
        holdsat = defaultdict(list)
        for t in range(0, len(self.trace.trace)):
            holdsat[t] = self.trace.trace[t].holdsat
        if remove_permpows:
            for t in range(0, len(observed) + 1):
                holdsat[t] = filter(lambda atom:
                                    not ((atom.arguments[0]).name
                                         in ["perm", "pow", "ipow", "gpow"]),
                                    holdsat[t])
        with open(self.output_file_name, 'w') as tfile:
            print(latex_gannt_header, file=tfile)
            print(r"\begin{longtable}{@{}r@{}}""\n", file=tfile)
            # set each chart fragment as a line in longtable to be breakable
            # over page boundaries
            for t in range(1, len(observed) + 1):
                if not occurred[t]:
                    continue  # ought not to happen
                print(
                    r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                    "{{{t}}}\n".format(t=len(observed) + 1), file=tfile)
                for x in occurred[t][:-1]:
                    l = (str(x.arguments[0]) + ": " +
                         str(x.arguments[1])).replace('_', '\_')
                    print("\\ganttmilestone{{{l}}}{{{f}}}\\ganttnewline"
                          .format(l=l, f=t - 1), file=tfile)
                # handle last event separately to drop \ganttnewline
                x = occurred[t][-1]
                l = (str(x.arguments[0]) + ": " +
                     str(x.arguments[1])).replace('_', '\_')
                print("\\ganttmilestone{{{l}}}{{{f}}}"
                      .format(l=l, f=t - 1), file=tfile)
                print(r"\end{ganttchart}\\[-0.7em]""\n", file=tfile)
            facts = invert(holdsat)
            keys = sorted(facts, key=lambda atom: atom.arguments[0].name)
            for f in keys:
                print(
                    r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                    "{{{t}}}\n".format(t=len(observed) + 1), file=tfile)
                i = facts[f][0]
                l = (str(f.arguments[0]) + ": " +
                     str(f.arguments[1])).replace('_', '\_')
                print("\\ganttbar{{{label}}}{{{start}}}{{{finish}}}"
                      .format(label=l, start=i, finish=i), file=tfile)
                for t in facts[f][1:]:
                    print("\\ganttbar{{}}{{{start}}}{{{finish}}}"
                          .format(start=t, finish=t), file=tfile)
                print(r"\end{ganttchart}\\[-0.7em]""\n", file=tfile)
            print(r"\end{longtable}""\n"
                  r"\end{document}", file=tfile)
