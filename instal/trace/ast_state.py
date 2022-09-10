##-- imports
from __future__ import annotations

import logging as logmod
from dataclasses import replace

import instal.interfaces.ast as iAST
import simplejson as json
from clingo import Symbol
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.trace import State_i
from instal.parser.parse_funcs import TERM

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalASTState(State_i):
    """ A workable representation of a single time Instal Model time step
    Collects everything that `holdsat`, `occurred` and was `observed`
    at a step.

    Representation of Terms: instal.interfaces.ast.TermAST

    """

    def __repr__(self) -> str:
        result = []
        result.append(f"-- Model Timestep {self.timestep}.")
        result.append("Active Fluents: ")
        max_key = max(len(x) for x in self.holdsat.keys())
        for k, v in self.holdsat.items():
            if not bool(v):
                continue
            v_str = " ".join(str(x) for x in v)
            result.append(f"{k:<{max_key}}: {v_str}")

        result.append("")
        result.append("Occurred Events: ")
        if bool(self.occurred):
            result.append(" ".join(str(x) for x in self.occurred))

        result.append("")
        result.append("Observed Events: ")
        if bool(self.observed):
            result.append(" ".join(str(x) for x in self.observed))

        if bool(self.rest):
            result.append("")
            result.append(f"Misc Terms: {len(self.rest)}")
            result.append(" ".join(str(x) for x in self.rest))

        result.append("")

        return "\n".join(result)



    def to_json(self) -> dict:
        state_dict = {
            "timestep" : self.timestep,
            "occurred" : [str(x) for x in self.occurred],
            "observed" : [str(x) for x in self.observed],
            "holdsat"  : {},
            "rest"     : [str(x) for x in self.rest]
        }

        for k, v in self.holdsat.items():
            state_dict['holdsat'][k] = [str(x) for x in v]

        return state_dict

    def __contains__(self, term) -> bool:
        try:
            if int(term.params[-1].value) != self.timestep:
                term = iAST.TermAST(term.value,
                                    params=(term.params[:-1]
                                            + [iAST.TermAST(str(self.timestep))])
                                    )
        except ValueError as err:
            return False

        match term.value:
            case "holdsat":
                return term in self.fluents
            case "occurred":
                return term in self.occurred
            case "observed":
                return term in self.observed
            case _:
                return term in self.rest

    def check(self, conditions) -> bool:
        return False
    def insert(self, term:str|Symbol|iAST.TermAST):
        if not isinstance(term, iAST.TermAST):
            term = TERM.parse_string(str(term))[0]

        assert(isinstance(term, iAST.TermAST))
        try:
            step = int(term.params[-1].value)
            if step != self.timestep:
                raise ValueError()
        except ValueError as err:
            logging.debug("State_i %s: Ignoring: %s", self.timestep, term)
            return

        match term.value:
            case "holdsat" if term.params[0].value in self.holdsat:
                self.holdsat[term.params[0].value].append(term)
            case "holdsat":
                self.holdsat["other"].append(term)
            case "occurred":
                self.occurred.append(term)
            case "observed":
                self.observed.append(term)
            case _:
                self.rest.append(term)




    def filter(self, *args):
        return False
