
##-- imports
from __future__ import annotations

import logging as logmod
import warnings
import abc
from collections import defaultdict
from typing import IO, List

from clingo import parse_term
from instal import InstalFile
##-- end imports

logging = logmod.getLogger(__name__)


class ClingoWrapper(metaclass=abc.ABCMeta):
    """
    An wrapper around clingo to simplify solving
    """
    ctl = None

    def __init__(self, model_files:List[InstalFile], domain_facts:defaultdict(set), verbose:int=0):
        if not self.ctl:  # Requires self.ctl to be set by subclass
            raise NotImplementedError

        for x in model_files:
            x.seek(0)
            logging.info("loading: ", x.name)
            self.ctl.load(x.name)

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

        logging.info("initialization complete")

    @abc.abstractmethod
    def solve(self, events: list): pass
