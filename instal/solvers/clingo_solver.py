
##-- imports
from __future__ import annotations

import logging as logmod
import os
import time
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import IO, List

import clingo
import instal
from clingo import Control, Function, Number, Symbol, parse_term
from instal.interfaces.ast import InitiallyAST, TermAST, QueryAST, DomainSpecAST
from instal.interfaces.solver import SolverWrapper, InstalModelResult
from instal.interfaces.state import Trace

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
        assert(self.program or bool(self.input_files))

        self.options = self.options or ['-n', str(1),
                                        '-c', f'horizon={self.length}']

        self.init_solver()

    def init_solver(self):
        self.ctl = Control(self.options)

        for path in self.input_files:
            logging.info("Clingo Loading: %s", path)
            assert(path.exists())
            self.ctl.load(str(path))

        try:
            self.ctl.add("base", [], self.program)
        except Exception as err:
            logging.exception("Clingo Failed to add Program")
            logging.debug(self.program)
            raise err

        logging.info("Clingo initialization complete")

    def solve(self, events:None|list[QueryAST|Symbol]=None, situation:None|list[QueryAST|Symbol]=None, fresh=False) -> int:
        events    = events or []
        situation = situation or []

        if fresh:
            self.init_solver()

        for x in (situation + events):
            logging.debug("assigning: %s", x)
            match x:
                case TermAST():
                    for sym in self.ast_to_clingo(x):
                        self.ctl.assign_external(sym, True)
                case Symbol():
                    self.ctl.assign_external(x, True)
                case _:
                    raise Exception("Unrecognized situation fact")

        def on_model_cb(model):
            """
            Handler for clingo finding a matching model for the program
            note: model destroyed on exit/reallocated in clingo,
            so information is copied into InstalModelResult to be processed
            later.
            """
            self.results.append(InstalModelResult(model.symbols(atoms=True),
                                                  model.symbols(shown=True),
                                                  model.cost,
                                                  model.number,
                                                  model.optimality_proven,
                                                  model.type))



        logging.info("Grounding Program")
        self.ctl.ground([("base", [])])
        logging.info("Running Program")
        result = self.ctl.solve(on_model=on_model_cb)

        logging.info("There are %s answer sets", len(self.results))
        return len(self.results)


    @property
    def metadata(self):
        return {
            "pid"            : os.getpid(),
            "source_files"   : [str(x) for x in self.input_files],
            "timestamp"      : self.timestamp,
            "mode"           : "multi_shot",
            "current_result" : self.current_answer,
            "result_size"    : len(self.results),
            "version"        : instal.__version__,
            "clingo_version" : clingo.__version__
        }


    def ast_to_clingo(self, *asts:TermAST) -> list[Symbol]:
        logging.debug("Converting to Clingo Symbols: %s", asts)
        results = []
        for ast in asts:
            match ast:
                case InitiallyAST():
                    assert(not bool(ast.conditions))
                    for fact in ast.body:
                        results.append(Function("holdsat",
                                                [parse_term(str(fact)),
                                                 Function(ast.inst)]))
                case QueryAST():
                    time = ast.time if ast.time else 0
                    event = parse_term(str(ast.head)) + [Number(time)]
                    results.append(Function("extObserved", event))
                    results.append(Function("_eventSet", [Number(time)]))

                case DomainSpecAST():
                    for fact in ast.body:
                        assert(not bool(ast.head.params))
                        results.append(Function(str(ast.head.value),
                                                [parse_term(str(x) for x in ast.body)]))

                case TermAST():
                    results.append(parse_term(str(ast)))


        return results
