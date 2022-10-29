
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

    def check(self, asts):
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

    def visit(self, node):
        """Visit a node."""
        assert(isinstance(node, iAST.InstalAST))
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        logging.debug("Visiting Node %s with %s", node, visitor)
        return visitor(node)

    def generic_visit(self, node):
        logging.info("Generic Visit Called, doing nothing: %s", node)

    def visit_all(self, nodes:list[iAST.InstalAST]):
        for x in nodes:
            self.visit(x)

    def visit_TermAST(self, node):
        self.uses[node.signature].append(node)
        self.visit_all(node.params)

    def visit_ConditionAST(self, node):
        self.visit(node.head)
        if node.rhs is not None:
            self.users[node.rhs.signature].append(node)

    def visit_InitiallyAST(self, node):
        self.visit_all(node.body + node.conditions)

    def visit_QueryAST(self, node):
        self.visit(node.head)
        self.visit_all(node.conditions)

    def visit_DomainSpecAST(self, node):
        self.visit(node.head)
        self.visit_all(node.body)


    ##-- inst visiting
    def visit_InstitutionDefAST(self, node):
        ##-- record declarations
        for declar in node.events + node.fluents:
            self.declarations[declar.head.signature] = declar
            self.visit_all(declar.head.params)

        for typeDec in node.types:
            self.declarations[typeDec.head.signature] = typeDec


        ##-- end record declarations

        # Record uses
        self.visit_all(node.initial + node.rules)

    def visit_BridgeDefAST(self, node):
        self.visit_InstitutionDefAST(node)

    ##-- end inst visiting

    ##-- rule visiting
    def visit_RuleAST(self, node):
        self.visit(node.head)
        self.visit_all(node.body + node.conditions)

    def visit_GenerationRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_InertialRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_TransientRuleAST(self, node):
        self.visit_RuleAST(node)

    ##-- end rule visiting
