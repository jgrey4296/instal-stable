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
        for varname in self.found_vars:
            pass

    def action_DomainSpecAST(self, visitor, node):
        self.found_types[node.head.signature].append(node)

    def action_TermAST(self, visitor, node):
        if node.is_var:
            self.found_vars[node.signature].append(node)
