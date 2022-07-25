
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
from instal import InstalFile, instal_file_name
from instal.interfaces.solver_wrapper import SolverWrapper
from instal.state.InstalStateTrace import InstalStateTrace
from insta.interfaces.ast import InitiallyAST, TermAST

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class ClingoOracle(SolverWrapper):
    """
    An Oracle that uses Clingo as the solver
    """

    options : list[str] = field(kw_only=True, default_factory=list)
    ctl : None|Control = field(init=False, default=None)

    def __post_init__(self, domain_facts:defaultdict(set)):
        clingo_options = self.options or ['-n', str(number),
                                          '-c', f'horizon={self.length}']

        self.ctl = Control(clingo_options)

        for path in self.input_files:
            logging.info("loading: %s", path)
            assert(path.exists())
            self.ctl.load(str(path))

        parts = []
        for typename, literals in domain_facts.items():
            for l in literals:
                parts += [(typename, [parse_term(l)])]
        logging.info("grounding: ", parts + [("base", [])])
        self.ctl.ground(parts + [("base", [])])
        logging.debug("grounded")

        signature_types   = [s[0] for s in self.ctl.symbolic_atoms.signatures]
        from_domain_types = [d for d in domain_facts]
        # Testing for type names in domain file not in grounded file
        for d in from_domain_types:
            if d not in signature_types:
                warnings.warn(f"WARNING: Type {d} in domain file is not in grounded model.")

        logging.info("Clingo initialization complete")

    def solve(self, events: List[Symbol]) -> List[InstalStateTrace]:
        self.observations = events
        self.cycle        = self.length

        for x in (self.observations + self.holdsat):
            logging.debug("assigning: %s", x)
            self.ctl.assign_external(x, True)

        def on_model_cb(model):
            new_model = {
                'symbols' : model.symbols(atoms=True),
                'cost'    : model.cost,
                'number'  : model.number
                'optimal' : model.optimality_proven,
                'type'    : model.type
                }

            self.results.append(new_model)
            if model.number() >= self.max_result:
                logging.warning("Max Result count reached, interrupting clingo")
                self.ctx.interrupt()
            ## note: model destroyed on exit/reallocated in clingo

        finished = False
        def on_finish_cb(sr):
            """
            hack: with the removal of solve_iter from clingo,
            and not using an asyncio design,
            this is the best I can think of.
            """
            finished = True

        result = self.ctl.solve(on_model=on_model_cb,
                                on_finish=on_finish_cb)

        while not finished:
            logging.warning("Solve not finished, waiting")
            time.sleep(5)

        logging.info("There are %s answer sets", len(self.results))
        # TODO convert to state traces
        return self.results

    def report(self, model_num:None|int=None) -> list[str]:
        # TODO: This is a massive bottleneck.
        model_num = model_num or self.max_result
        atoms     = defaultdict(list)
        model     = self.results[model_num]
        logging.debug("FULL ATOM PRINTING\n---------------")
        for atom in model.symbols(atoms=True):
            logging.debug(atom)

        for atom in model.symbols(shown=True):
            logging.debug(atom)
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

    @property
    def metadata(self):
        return {
            "pid": os.getpid(),
            "source_files": [str(x) for x in self.input_files],
            "timestamp": self.timestamp,
            "mode": "multi_shot",
            "max_result": self.max_result,
            "current_result" : self.current_answer,
            "result_size": len(self.results)
            "version" : instal.__version__,
        }
