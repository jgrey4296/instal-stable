##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class InstitutionStructureChecker(InstalChecker_i):

    def check(self, asts):
        for inst in asts:
            if not isinstance(inst, iAST.InstitutionDefAST):
                continue

            if not bool(inst.fluents):
                self.warning("Institution has no fluents", inst)

            if not bool(inst.events):
                self.warning("Institution has no events", inst)

            if not bool(inst.types):
                self.warning("Institution has no types", inst)

            if not bool(inst.rules):
                self.warning("Institution has no rules", inst)

            if not bool(inst.initial):
                self.warning("Institution has no initial facts", inst)


    ##-- end misc
