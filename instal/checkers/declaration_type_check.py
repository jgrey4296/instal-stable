##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i
import instal.interfaces.ast as iAST

##-- end imports

@dataclass
class DeclarationTypeCheck(InstalChecker_i):
    """ Check the types used in rules

    augmented with a generated ast node visitor
    """

    found_types : dict[str, list[iAST.DomainSpecAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    found_vars  : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def check(self, asts):
        # accumulate
        self.visit_all(asts)

        # check
        for varname in self.found_vars:
            pass


    def visit(self, node):
        """Visit a node."""
        assert isinstance(node, iAST.InstalAST)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        logging.info('Generic Visit Called, doing nothing: %s', node)

    def visit_all(self, nodes: list[iAST.InstalAST]):
        for x in nodes:
            self.visit(x)

    def visit_BridgeDefAST(self, node):
        self.visit_InstitutionDefAST(node)

    def visit_ConditionAST(self, node):
        self.visit(node.head)
        if node.rhs:
            self.visit(node.rhs)

    def visit_DomainSpecAST(self, node):
        self.found_types[node.head.signature].append(node)


    def visit_EventAST(self, node):
        self.visit(node.head)

    def visit_FluentAST(self, node):
        self.visit(node.head)

    def visit_GenerationRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_InertialRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_InitiallyAST(self, node):
        self.visit_all(node.body + node.conditions)

    def visit_InstitutionDefAST(self, node):
        self.visit_all(node.types + node.fluents + node.events + node.rules + node.initial)


    def visit_QueryAST(self, node):
        self.visit(node.head)
        self.visit_all(node.conditions)

    def visit_RuleAST(self, node):
        self.visit(node.head)
        self.visit_all(node.body + node.conditions)

    def visit_TermAST(self, node):
        if node.is_var:
            self.found_vars[node.signature].append(node)

        self.visit_all(node.params)

    def visit_TransientRuleAST(self, node):
        self.visit_RuleAST(node)
