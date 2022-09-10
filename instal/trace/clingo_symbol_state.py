##-- imports
from __future__ import annotations

import logging as logmod

import simplejson as json
from clingo import Symbol, SymbolType, parse_term
from instal.interfaces.solver import InstalModelResult
from instal.interfaces.trace import State_i

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
                "occurred" : [],
                "observed" : [],
                "holdsat" : {
                    "perms" : [],
                    "pows" : [],
                    "tpows" : [],
                    "ipows" : [],
                    "gpows" : [],
                    "obls" : [],
                    "fluents" : []
                    }
                }
        for o in self.occurred:
            state_dict["occurred"].append(symbol_to_atom_list(o))
        for o in self.observed:
            state_dict["observed"].append(symbol_to_atom_list(o))
        for h in self.holdsat:
            lst_atom = symbol_to_atom_list(h)
            key = lst_atom[1][0][0]
            if key == "perm":
                state_dict["holdsat"]["perms"].append(lst_atom )
            elif key == "pow":
                state_dict["holdsat"]["pows"].append(lst_atom )
            elif key == "tpow":
                state_dict["holdsat"]["tpows"].append(lst_atom )
            elif key == "gpow":
                state_dict["holdsat"]["gpows"].append(lst_atom )
            elif key == "ipow":
                state_dict["holdsat"]["ipows"].append(lst_atom )
            elif key == "obl":
                state_dict["holdsat"]["obls"].append(lst_atom)
            else:
                state_dict["holdsat"]["fluents"].append(lst_atom)

        return { "state" : state_dict,
                 "metadata" : self.metadata }


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