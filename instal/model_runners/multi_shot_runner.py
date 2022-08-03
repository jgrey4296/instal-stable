
##-- imports
from __future__ import annotations

import logging as logmod
import time
from dataclasses import InitVar, dataclass, field
from typing import IO, List

from clingo import Function, Symbol
from instal.compiler.joint_compiler import InstalJointCompiler
from instal.errors import InstalRuntimeError
from instal.interfaces.model_runner import InstalModelRunner
from instal.parser.pyparse_institution import InstalPyParser
from instal.reporters.text_reporter import InstalTextReporter
from instal.solvers.clingo_solver import ClingoSolver

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class InstalMultiShotRunner(InstalModelRunner):
    """

    """

    parser   : InstalParser   = field(default_factory=InstalPyParser)
    compiler : InstalCompiler = field(default_factory=InstalJointCompiler)
    solver   : SolverWrapper  = field(default_factory=ClingoSolver)
    reporter : InstalReporter = field(default_factory=InstalTextReporter)

    checker    : None|InstalChecker = field(default=None, kw_only=True)

    timestamp : float               = field(default_factory=time.time)


    def solve(self, query_events:List[Symbol]=None):
        observed       = []

        for i, e in enumerate(query_events):
            observed += [Function('extObserved', [e.arguments[0], i]),
                         Function('_eventSet', [i])]

        # note: events is a list of Fun not strings
        output = self.solver.solve(observed)

        if not bool(self.solver.answersets):
            raise InstalRuntimeError("Solver produced 0 answer sets. This usually means:\n"
                                     "- You have included additional .lp files with constraints in them."
                                     "- You have forgotten to ground types that exist in your institutions.")

        self.answersets = self.solver.answersets

        return self.answersets
