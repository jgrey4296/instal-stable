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

    terms       : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    events      : dict[str, iAST.EventAST]      = field(init=False, default_factory=dict)
    obligations : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    fluents     : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def action_TermAST(self, visitor, node):
        """
        Track deontic terms
        ie: perm(anEvent), pow(anEvent).
        """
        if node.value not in DEONTICS:
            return

        if not node.value == "obl":
            self.terms[node.params[0].signature].append(node)
        else:
            obl_key = "-".join([x.signature for x in node.params])
            self.terms[obl_key].append(node)

    def action_FluentAST(self, visitor, node):
        """
        track obligation fluents
        """
        if not node.annotation == iAST.FluentEnum.obligation:
            return

        if not node.head.value == "obl":
            self.delay_error("An Obligation Fluent isn't wrapped in `obl`", node)

        if len(node.head.params) != 4:
            self.delay_error("An Obligation Fluent doesn't have enough components", node)

        obl_key = "-".join([x.signature for x in node.head.params])
        self.fluents[obl_key].append(node)


    def action_EventAST(self, visitor, node):
        if node.annotation != iAST.EventEnum.institutional:
            return

        self.events[node.head.signature] = node

    def validate(self):
        """
        Ensure that all terms marked with deontic qualifiers,
        are institutional events,
        or obligations
        """
        deontic_terms  = set(self.terms.keys())
        event_set      = self.events.keys()
        obligation_set = self.fluents.keys()

        for term in (deontic_terms - event_set - obligation_set):
            for ast in self.terms[term]:
                self.delay_error("Deontic Qualifier is not applied to an institutional event", ast)
