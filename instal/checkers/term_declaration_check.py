
##-- imports
import logging as logmod
import warnings
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import instal.interfaces.ast as iAST
import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i
from insta.checkers.visitor import InstalBaseASTVisitor
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class TermDeclarationCheck(InstalChecker_i):
    """ Check all terms are declared, and use consistent number of arguments
    check no term starts with a number,
    and no Variable has params

    Augmented with util.generate_visitors
    """

    declarations : dict[str, iAST.TermAST]   = field(init=False, default_factory=dict)
    uses         : dict[str, [iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def get_actions(self):
        visit_actions = {


            }
        return visit_actions


    def check(self):
        """
        Check all Terms, by visiting every node.
        Declarations and uses are recorded as signatures in the classic prolog style of name/{numArgs}.
        Mismatches are then reported
        """


        ##-- record declarations and visit the asts
        self.visit_all(asts)
        ##-- end record declarations and visit the asts

        ##-- report on mismatches
        for termSig in set(self.declarations.keys()).difference(self.uses.keys()):
            term = self.declarations[termSig]
            self.warning("Term declared without use", term)

        for termSig in set(self.uses.keys()).difference(self.declarations.keys()):
            terms = self.uses[termSig]
            for useTerm in terms:
                self.error("Term used without declaration", useTerm)

        ##-- end report on mismatches



    def action_TermAST(self, visitor, node):
        self.uses[node.signature].append(node)

    def action_InstitutionDefAST(self, visitor, node):
        for declar in node.events + node.fluents:
            self.declarations[declar.head.signature] = declar

        for typeDec in node.types:
            self.declarations[typeDec.head.signature] = typeDec
