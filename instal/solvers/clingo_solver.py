
##-- imports
from __future__ import annotations

from pathlib import Path
import logging as logmod
import os
import time
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from typing import IO, List

import instal
from clingo import Control, Function, Symbol
from instal.interfaces.solver_wrapper import SolverWrapper
from instal.interfaces.state import Trace
from instal.interfaces.ast import InitiallyAST, TermAST
from instal.util.misc import InstalModelResult

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class ClingoSolver(SolverWrapper):
    """
    An Oracle that uses Clingo as the solver
    """

    options : list[str]    = field(kw_only=True, default_factory=list)
    ctl     : None|Control = field(init=False, default=None)

    def __post_init__(self):
        clingo_options = self.options or ['-n', str(number),
                                          '-c', f'horizon={self.length}']

        self.ctl = Control(clingo_options)

        for path in self.input_files:
            logging.info("Clingo Loading: %s", path)
            assert(path.exists())
            self.ctl.load(str(path))

        logging.info("Clingo initialization complete")

    def solve(self, events: List[Symbol]) -> List[dict]:
        self.observations = events
        self.cycle        = self.length

        for x in (self.observations + self.holdsat):
            logging.debug("assigning: %s", x)
            self.ctl.assign_external(x, True)

        def on_model_cb(model):
            self.results.append(InstalModelResult(model.symbols(atoms=True),
                                                  model.symbols(shown=True),
                                                  model.cost,
                                                  model.number,
                                                  model.optimality_proven,
                                                  model.type))

            self.results.append(new_model)
            ## note: model destroyed on exit/reallocated in clingo


        logging.info("Grounding Program")
        ctl.ground([("base", [])])
        logging.info("Running Program")
        result = self.ctl.solve(on_model=on_model_cb)

        logging.info("There are %s answer sets", len(self.results))
        return self.results

    @property
    def metadata(self):
        return {
            "pid"            : os.getpid(),
            "source_files"   : [str(x) for x in self.input_files],
            "timestamp"      : self.timestamp,
            "mode"           : "multi_shot",
            "max_result"     : self.max_result,
            "current_result" : self.current_answer,
            "result_size"    : len(self.results),
            "version"        : instal.__version__,
        }
