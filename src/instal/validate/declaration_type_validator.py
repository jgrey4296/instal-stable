##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
import instal.interfaces.ast as iAST

##-- end imports

@dataclass
class DeclarationTypeValidator(InstalValidator_i):
    """ Validator the types used in rules

    augmented with a generated ast node visitor
    """

    found_types : dict[str, list[iAST.DomainSpecAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    found_vars  : dict[str, list[iAST.TermAST]]       = field(init=False, default_factory=lambda: defaultdict(list))

    def validate(self):
        # solve the constriants
        pass

    def action_DomainSpecAST(self, visitor, node):
        self.found_types[node.head.signature].append(node)
        # TODO store the values as well

    def action_FluentAST(self, visitor, node):
        # TODO map declarations to types
        pass

    def action_EventAST(self, visitor, node):
        # TODO map declarations to types
        pass

    def action_RuleAST(self, visitor, node):
        # TODO Generate constraints for the rule
        # values map to types
        # argvars map to declared types of fluents and events.
        pass
