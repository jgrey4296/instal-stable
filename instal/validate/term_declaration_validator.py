
##-- imports
import logging as logmod
import warnings
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import instal.interfaces.ast as iAST
import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class TermDeclarationValidator(InstalValidator_i):
    """ Validate all terms are declared, and use consistent number of arguments
    validate no term starts with a number,
    and no Variable has params

    Augmented with util.generate_visitors
    """

    declarations : dict[str, iAST.TermAST]   = field(init=False, default_factory=dict)
    uses         : dict[str, [iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))


    def validate(self):
        """
        Validate all Terms, by visiting every node.
        Declarations and uses are recorded as signatures in the classic prolog style of name/{numArgs}.
        Mismatches are then reported
        """

        ##-- report on mismatches
        for termSig in set(self.declarations.keys()).difference(self.uses.keys()):
            term = self.declarations[termSig]
            self.delay_warning("Term declared without use", term)

        for termSig in set(self.uses.keys()).difference(self.declarations.keys()):
            terms = self.uses[termSig]
            for useTerm in terms:
                self.delay_error("Term used without declaration", useTerm)

        ##-- end report on mismatches


    def action_TermAST(self, visitor, node):
        # TODO this counts everything as a use, so is meaningless
        self.uses[node.signature].append(node)

    def action_InstitutionDefAST(self, visitor, node):
        self.declarations[node.head.signature] = node

        for declar in node.events + node.fluents:
            self.declarations[declar.head.signature] = declar

        for typeDec in node.types:
            self.declarations[typeDec.head.signature] = typeDec
