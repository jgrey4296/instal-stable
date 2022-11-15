##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
from instal.interfaces import ast as iAST

from instal.defaults import DEONTICS

##-- end imports

@dataclass
class DeonticValidator(InstalValidator_i):
    """ validator perm/pow/obl/viol only apply to institutional events """

    terms  : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    events : dict[str, iAST.EventAST]      = field(init=False, default_factory=dict)

    def action_TermAST(self, visitor, node):
        if node.value not in DEONTICS:
            return

        self.terms[node.params[0].signature].append(node)

    def action_EventAST(self, visitor, node):
        if node.annotation != iAST.EventEnum.institutional:
            return

        self.events[node.head.signature] = node

    def validate(self):
        deontic_terms = set(self.terms.keys())
        event_set     = self.events.keys()

        for term in (deontic_terms - event_set):
            for ast in self.terms[term]:
                self.delay_error("Deontic Qualifier is not applied to an institutional event", ast)
