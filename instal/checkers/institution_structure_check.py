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
    """ Check components of institutions are defined """

    def get_actions(self):
        return {
            iAST.InstitutionDefAST: {self.action_InstitutionDefAST}
            }


    def action_InstitutionDefAST(self, visitor, node):
        if not bool(node.fluents):
            self.warning("Institution has no fluents", node)

        if not bool(node.events):
            self.warning("Institution has no events", node)

        if not bool(node.types):
            self.warning("Institution has no types", node)

        if not bool(node.rules):
            self.warning("Institution has no rules", node)

        if not bool(node.initial):
            self.warning("Instiitution has no initial facts", node)
