
##-- imports
from __future__ import annotations

import logging as logmod
import os
import time
from functools import partial
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import IO, List

import clingo
import instal
from clingo import Control, Function, Number, Symbol, parse_term
from instal.interfaces.ast import InitiallyAST, TermAST, QueryAST, DomainSpecAST, InstalAST
from instal.interfaces.solver import SolverWrapper_i, InstalModelResult

##-- end imports

##-- logging
logging       = logmod.getLogger(__name__)
clingo_logger = logmod.getLogger(__name__ + ".ffi.clingo")
##-- end logging

def clingo_intercept_logger(code, msg):
    """
    Intercepts messages from clingo, and controls
    the logging of them
    """
    msg = msg.replace("\n", "")
    match code:
        case clingo.MessageCode.AtomUndefined:
            clingo_logger.debug(msg)
        case clingo.MessageCode.RuntimeError:
            clingo_logger.exception(msg)
        case _:
            clingo_logger.info(msg)

def model_cb(self, model:clingo.Model):
    """
    Partial callback for clingo.
    Used for storing models.
    *Must* be constructed using functools.partial
    with 'self' bound to the SolverWrapper

    NOTE: Clingo Models are destroyed/reallocated on exit of the callback,
    Which is why we don't just store the model itself
    """
    self.results.append(InstalModelResult(model.symbols(atoms=True),
                                            model.symbols(shown=True),
                                            model.cost,
                                            model.number,
                                            model.optimality_proven,
                                            model.type))

@dataclass
class ClingoSolver(SolverWrapper_i):
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

    def __repr__(self):
        return "[Clingo Solver: {}; Opts: {}; Models: {}]".format(self.ctl is not None,
                                                                  " ".join(self.options),
                                                                  len(self.results))
    def init_solver(self):
        self.ctl = Control(self.options, logger=clingo_intercept_logger)

        for path in self.input_files:
            logging.debug("Clingo Loading: %s", path)
            assert(path.exists())
            self.ctl.load(str(path))

        try:
            self.ctl.add("base", [], self.program)
        except Exception as err:
            logging.exception("Clingo Failed to add Program")
            logging.debug(self.program)
            raise err

        logging.info("Clingo initialization complete")

    def solve(self, events:None|list[str|QueryAST|Symbol]=None, situation:None|list[str|InitiallyAST|Symbol]=None, fresh=False) -> int:
        events    = events    or []
        situation = situation or []

        if fresh:
            self.init_solver()

        logging.debug("Grounding Program")
        self.ctl.ground([("base", [])])

        for x in (situation + events):
            logging.debug("assigning: %s", x)
            match x:
                case InstalAST():
                    for sym in self.ast_to_clingo(x):
                        self.ctl.assign_external(sym, True)
                case Symbol():
                    self.ctl.assign_external(x, True)
                case str():
                    self.ctl.assign_external(parse_term(x), True)
                case _:
                    raise Exception("Unrecognized situation fact")

        on_model_cb = partial(model_cb, self)


        logging.info("Running Program")
        self.ctl.solve(on_model=on_model_cb)

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
                        results.append(Function("extHoldsat",
                                                [parse_term(str(fact)),
                                                 parse_term(str(ast.inst))]))
                case QueryAST():
                    time = ast.time if ast.time else 0
                    event = parse_term(str(ast.head))
                    results.append(Function("extObserved", [event, Number(time)]))
                    results.append(Function("_eventSet", [Number(time)]))

                case DomainSpecAST():
                    for fact in ast.body:
                        assert(not bool(ast.head.params))
                        results.append(Function(str(ast.head.value),
                                                [parse_term(str(x) for x in ast.body)]))

                case TermAST():
                    results.append(parse_term(str(ast)))
                case _:
                    raise Exception("Unrecognised AST sent to solver: ", ast)


        return results
