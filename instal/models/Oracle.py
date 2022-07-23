
##-- imports
from __future__ import annotations

import logging as logmod
import os
import time
from collections import defaultdict
from typing import IO, List

import instal
from clingo import Control, Function, Symbol
from instal import InstalFile, instal_file_name
from instal.interfaces.clingo_wrapper import ClingoWrapper
from instal.state.InstalStateTrace import InstalStateTrace
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class Oracle(ClingoWrapper):
    """
        Oracle
        The ClingoWrapper for multi shot solves.
        A significant chunk of this code is legacy and thus fragile.
    """

    # TODO refactor with InstalOptionGroup
    def __init__(self,
                 initially : List[Symbol],
                 model_files : List[InstalFile],
                 domain_facts : defaultdict(set),
                 verbose : int=0,
                 length : int = 1,
                 number : int = 1,
                 answer_set : int = 0):

        self.answersets   = []
        self.cycle        = 0
        self.observations = None
        self.holdsat      = initially
        self.timestamp    = time.time()
        self.answer_set   = answer_set
        self.number       = number
        self.length       = length
        self.verbose      = verbose
        self.input_files  = model_files

        self.ctl = Control(['-n', str(number), '-c',
                            'horizon={0}'.format(self.length)])
        super(Oracle, self).__init__(
            model_files, domain_facts, verbose)

    def solve(self, events: List[Symbol]) -> List[InstalStateTrace]:
        models = {}
        self.observations = events
        for x in self.observations:
            if self.verbose > 2:
                print("assign", x)
            self.ctl.assign_external(x, True)
        for h in self.holdsat:
            self.ctl.assign_external(h, True)
        self.cycle = self.length
        answers = 0
        with self.ctl.solve_iter() as it:
            for m in it:
                new_model = {}
                atoms = []
                if self.answer_set > 0 and self.answer_set != answers + 1:
                    atoms = []
                else:
                    atoms = [self.holdsat] + self.process_answer_set(m)
                if len(m.cost) > 0:
                    new_model["cost"] = m.cost[0]
                new_model["atoms"] = atoms
                models[answers] = new_model
                answers += 1
        for k,v in models.items():
            self.answersets.append(InstalStateTrace.state_trace_from_list(v.get("atoms"),metadata=self.generate_json_metadata(k, answers,v.get("cost",0))))
        if self.verbose > 0:
            if answers == 1:
                print("There is 1 answer set")
            else:
                print("There are {} answer sets".format(answers))
        return self.answersets

    # Okay, the utility function doesn't work because this is a full trace
    # model.
    def process_answer_set(self, model):
        # TODO: This is a massive bottleneck.
        atoms = defaultdict(list)

        if self.verbose > 2:
            print("FULL ATOM PRINTING\n---------------")
        if self.verbose > 3:
            for atom in model.symbols(atoms=True):
                print(atom)
        for atom in model.symbols(shown=True):
            if self.verbose > 2:
                print(atom)
            if atom.name in ["observed", "occurred", "holdsat"]:
                what = Function(atom.name, atom.arguments[:-1])
                when = atom.arguments[-1].number
                if (atom.name == "observed") and (len(atom.arguments) == 2):
                    atoms[when + 1].append(what)
                if atom.name == "occurred":
                    atoms[when + 1].append(what)
                if atom.name == "holdsat":
                    atoms[when].append(what)
        out = []

        for k, v in sorted(atoms.items()):
            if k > 0:
                out.append(v)
        return out


    def generate_json_metadata(self, n, of,cost=0):
        metadata = {
            "pid": os.getpid(),
            "source_files": [instal_file_name(f) for f in self.input_files],
            "timestamp": self.timestamp,
            "mode": "multi_shot",
            "answer_set_n": n+1,
            "answer_set_of": of,
            "version" : instal.__version__,
            "cost" : cost
        }
        return metadata
