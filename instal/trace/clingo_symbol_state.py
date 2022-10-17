##-- imports
from __future__ import annotations

import logging as logmod

from clingo import Symbol, SymbolType, parse_term
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.trace import State_i

import instal.interfaces.ast as iAST

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalClingoState(State_i):
    """ A workable representation of a single time Instal Model time step
    Collects everything that `holdsat`, `occurred` and was `observed`
    at a step.

    Representation of Terms: clingo.Symbol.
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
        match term:
            case Symbol():
                pass
            case iAST.TermAST():
                term = parse_term(str(term))

        try:
            # coerce to current timestep
            if (term.arguments[-1].type is SymbolType.Number
                and term.arguments[-1].number != self.timestep):
               val    = term.name
               params = term.arguments[:-1] + [iAST.TermAST(self.timestep)]
               term   = parse_term(f"{val}({','.join(str(x) for x in params)})")

        except ValueError as err:
            return False

        match term.name:
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
        if not isinstance(term, Symbol):
            term = parse_term(str(term))

        assert(isinstance(term, Symbol))
        match (term.name, term.arguments[-1]):
            case _, step if step.type != SymbolType.Number:
                logging.debug("State_i %s: Ignoring: %s", self.timestep, term)
            case _, step if step.number != self.timestep:
                logging.debug("State_i %s: Ignoring: %s", self.timestep, term)
            case "holdsat", _ if term.arguments[0].name in self.holdsat:
                self.holdsat[term.arguments[0].name].append(term)
            case "holdsat", _:
                self.holdsat["other"].append(term)
            case "occurred", _:
                self.occurred.append(term)
            case "observed", _:
                self.observed.append(term)
            case _, _:
                self.rest.append(term)

    def filter(self, *args):
        return False
