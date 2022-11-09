##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class InstitutionStructureValidator(InstalValidator_i):
    """ Validator components of institutions are defined """


    def action_InstitutionDefAST(self, visitor, node):
        if not bool(node.fluents):
            self.delay_warning("Institution has no fluents", node)

        if not bool(node.events):
            self.delay_warning("Institution has no events", node)

        if not bool(node.types):
            self.delay_warning("Institution has no types", node)

        if not bool(node.rules):
            self.delay_warning("Institution has no rules", node)

        if not bool(node.initial):
            self.delay_warning("Instiitution has no initial facts", node)
