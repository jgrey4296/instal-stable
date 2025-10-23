
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

Sig = str

@dataclass
class TermDeclarationValidator(InstalValidator_i):
    """ Validate all terms are declared, and use consistent number of arguments
    validate no term starts with a number,
    and no Variable has params

    Augmented with util.generate_visitors
    """

    declarations   : dict[Sig, iAST.TermAST]       = field(init=False, default_factory=dict)
    uses           : dict[Sig, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    signature_alts : dict[str, set[Sig]]           = field(init=False, default_factory=lambda: defaultdict(list))


    def validate(self):
        for termSig in set(self.declarations.keys()).difference(self.uses.keys()):
            term = self.declarations[termSig]
            self.delay_warning("Term declared without use", term)

        for termSig in set(self.uses.keys()).difference(self.declarations.keys()):
            terms = self.uses[termSig]
            for useTerm in terms:
                if useTerm.value in self.signature_alts:
                    declared = ", ".join(self.signature_alts[useTerm.value])
                    msg = f"Term used without declaration, but these were: [ {declared} ]"
                else:
                    msg = "Term used without declaration"

                self.delay_error(msg, useTerm)

    def action_InstitutionDefAST(self, visitor, node):
        # An Institution is its own use
        self.declarations[node.head.signature] = node
        self.uses[node.head.signature].append(node)

        # Record all types and values
        for typeDec in node.types:
            self.declarations[typeDec.head.signature] = typeDec
            self.signature_alts[typeDec.head.value].append(typeDec.head.signature)

        # then declarations
        for declar in node.events + node.fluents:
            self.declarations[declar.head.signature] = declar
            self.signature_alts[declar.head.value].append(declar.head.signature)
            self._dfs_term_use(declar.head)

    def action_RuleAST(self, visitor, node):
        # for rule head, and body,
        # record uses
        self._dfs_term_use(node.head, *node.body)

    def action_ConditionAST(self, visitor, node):
        # record uses
        self._dfs_term_use(node.head, node.rhs)

    def _dfs_term_use(self, *terms):
        # types/values in declarations as args count as uses:
        # so a quick DFS on them
        queue = list(terms)
        while bool(queue):
            current = queue.pop()
            if current is None:
                continue

            assert(isinstance(current, iAST.TermAST))
            if bool(current.params):
                queue += current.params

            self.uses[current.signature].append(current)
