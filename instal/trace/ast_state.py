##-- imports
from __future__ import annotations

import logging as logmod

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

    def check(self, conditions : dict, verbose=2) -> bool:
        """Takes an InstAL trace and a set of conditions in the format:
            [
                { "holdsat" : [],
                  "occurred" : [],
                  "notholdsat" : [],
                  "notoccurred" : []
            ,
                { ... }
            ]

            Returns: 0 if the trace fits those conditions, +1 for each condition it doesn't meet.
            """
        errors = 0
        for h in conditions.get("holdsat", []):
            found = False
            t = parse_term(h)
            for a in self.holdsat:
                if a == t:
                    found = True
                    break
            if found:
                if verbose > 1:
                    print("Holds (correctly)", h)
            else:
                errors += 1
                if verbose > 0:
                    print("Doesn't hold (and should): ", h)

        for h in conditions.get("occurred", []):
            found = False
            t = parse_term(h)
            for a in self.occurred:
                if a == t:
                    found = True
                    break
            if found:
                if verbose > 1:
                    print("Occurred (correctly)", h)
            else:
                errors += 1
                if verbose > 0:
                    print("Didn't occur (and should have): ", h)

        for h in conditions.get("notholdsat", []):
            found = False
            t = parse_term(h)
            for a in self.holdsat:
                if a == t:
                    found = True
                    break
            if not found:
                if verbose > 1:
                    print("Doesn't Hold (correctly)", h)
            else:
                errors += 1
                if verbose > 0:
                    print("Holds (and shouldn't): ", h)

        for h in conditions.get("notoccurred", []):
            found = False
            t = parse_term(h)
            for a in self.occurred:
                if a == t:
                    found = True
                    break
            if not found:
                if verbose > 1:
                    print("Doesn't occur (correctly)", h)
            else:
                errors += 1
                if verbose > 0:
                    print("Occurs (and shouldn't): ", h)
        return errors

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
            case "occurred":
                self.occurred.append(term)
            case "observed":
                self.observed.append(term)
            case _:
                self.rest.append(term)
