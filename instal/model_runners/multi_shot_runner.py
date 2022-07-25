
##-- imports
from __future__ import annotations

import logging as logmod
import time
from typing import IO, List

from clingo import Function, Symbol
from instal import InstalFile
from instal.instalexceptions import InstalRuntimeError

from instal.interfaces.model_runner import InstalModelRunner
from instal.solvers.clingo_solver import ClingoSolver
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalMultiShotRunner(InstalModelRunner):
    """

    """

    # TODO refactor using InstalFileGroup and InstalOptionGroup
    def __init__(self,
                 ial_files:List[InstalFile],
                 bridge_files:List[InstalFile],
                 lp_files:List[InstalFile],
                 domain_files:List[InstalFile],
                 fact_files:List[InstalFile],
                 verbose:int=0,
                 answer_set:int=0,
                 length:int=1,
                 number:int=1):

            super(InstalMultiShotModel, self).__init__(ial_files,bridge_files,lp_files,domain_files,fact_files)
            self.timestamp = 0
            self.oracle    = ClingoSolver(self.initial_facts,self.model_files,self.domain_facts,verbose=verbose, length=length, answer_set=answer_set, number=number)
            self.verbose   = verbose # clean this up

    def solve(self, query_events:List[Symbol]):
        self.timestamp = time.time()
        observed       = []

        for i, e in enumerate(query_events):
            observed += [Function('extObserved', [e.arguments[0], i]),
                         Function('_eventSet', [i])]

        # note: events is a list of Fun not strings
        output = self.oracle.solve(observed)

        if not bool(self.oracle.answersets):
            raise InstalRuntimeError("Solver produced 0 answer sets. This usually means:\n"
                                     "- You have included additional .lp files with constraints in them."
                                     "- You have forgotten to ground types that exist in your institutions.")

        self.answersets = self.oracle.answersets

        return self.answersets
