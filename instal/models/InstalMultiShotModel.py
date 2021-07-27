import time
from typing import IO, List

from clingo import Function, Symbol

from instal.instalexceptions import InstalRuntimeError
from .InstalModel import InstalModel
from .Oracle import Oracle
from instal import InstalFile


class InstalMultiShotModel(InstalModel):
    """
        InstalMultiShotModel
        Deals with multi shot solving - instance of InstalModel.
        Used for instalquery.
    """

    def __init__(self,ial_files : List[InstalFile], bridge_files : List[InstalFile], lp_files : List[InstalFile],
        domain_files : List[InstalFile], fact_files : List[InstalFile],
        verbose : int = 0, answer_set : int = 0, length : int = 1, number : int = 1):

            super(InstalMultiShotModel, self).__init__(ial_files,bridge_files,lp_files,domain_files,fact_files)
            self.timestamp = 0
            self.oracle = Oracle(self.initial_facts,self.model_files,self.domain_facts,verbose=verbose, length=length, answer_set=answer_set, number=number)
            self.verbose = verbose # clean this up

    def solve(self, query_events : List[Symbol]):
        self.timestamp = time.time()
        observed = []
        for i, e in enumerate(query_events):
            observed += [Function('extObserved', [e.arguments[0], i]),
                         Function('_eventSet', [i])]
        # note: events is a list of Fun not strings
        output = self.oracle.solve(observed)
        of = len(self.oracle.answersets)
        if of == 0:
            raise InstalRuntimeError(
                "Solver produced 0 answer sets. This usually means:\n"
                "- You have included additional .lp files with constraints in them."
                "- You have forgotten to ground types that exist in your institutions.")

        self.answersets = self.oracle.answersets
        if of == 1 and self.verbose > 0:
            print(self.answersets[0].to_str(show_perms=(self.verbose>1),show_pows=(self.verbose>1), show_cross=(self.verbose>1)))
        return self.answersets
