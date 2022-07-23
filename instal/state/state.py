
##-- imports
from __future__ import annotations

import logging as logmod
from typing import Dict, List

from clingo import Symbol, parse_term
from instal.parser.atom_parser import (atom_list_to_symbol, atom_sorter,
                                       symbol_to_atom_list)
from isnta.interfaces.trace import State
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalState(State):

    @classmethod
    def from_json(cls, json : dict) -> "InstalState":
        state = InstalState()
        state.metadata = json["metadata"]
        for a in json["state"]["occurred"]:
            state.occurred.append(atom_list_to_symbol(a))
        for a in json["state"]["observed"]:
            state.observed.append(atom_list_to_symbol(a))
        for k, v in json["state"]["holdsat"].items():
            for a in v:
                state.holdsat.append(atom_list_to_symbol(a))
        return state

    @classmethod
    def from_list(cls, lst : List[Symbol], metadata : dict = None) -> "InstalState":
        state = InstalState()
        state.metadata = metadata
        for a in lst:
            if a.name == "holdsat":
                state.holdsat.append(a)
            elif a.name == "occurred":
                state.occurred.append(a)
            elif a.name == "observed":
                state.observed.append(a)
        return state



    def __str__(self, show_perms=True, show_pows=True, show_cross=True) -> str:
        out_str = ""
        for h in atom_sorter(self.holdsat):
            lst_atom = symbol_to_atom_list(h)
            if not ((lst_atom[1][0][0] == "perm" and not show_perms) or (lst_atom[1][0][0] == "pow" and not show_pows) or (((lst_atom[1][0][0] == "ipow") or (lst_atom[1][0][0] == "tpow") or (lst_atom[1][0][0] == "gpow")) and not show_cross)):
                out_str += str(h) + "\n"
        for o in atom_sorter(self.occurred):
            out_str += str(o) + "\n"
        for o in atom_sorter(self.observed):
            out_str += str(o) + "\n"
            # TODO This is a horrible hack; deal with the incorrect output from
            # query first. (The break thing to only get one observed that is.)
            break
        return out_str
    def to_json(self) -> Dict:
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


    def to_list(self) -> List[Symbol]:
        return [a for a in self.occurred+self.observed+self.holdsat]


    def to_solver(self) -> str:
        pass

    def check(self, conditions : dict, verbose=2):
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
