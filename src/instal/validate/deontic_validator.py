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

obligations = {iAST.FluentEnum.obligation,
               iAST.FluentEnum.achievement_obligation,
               iAST.FluentEnum.maintenance_obligation}

@dataclass
class DeonticValidator(InstalValidator_i):
    """ validator perm/pow/obl/viol only apply to institutional inst_events """

    deontic_terms : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    inst_events   : dict[str, iAST.EventAST]      = field(init=False, default_factory=dict)
    obligations   : dict[str, iAST.FluentAST]     = field(init=False, default_factory=dict)
    potential_obl : dict[str, list[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def action_TermAST(self, visitor, node):
        """
        Track deontic terms
        ie: perm(anEvent), pow(anEvent).
        """
        if node.value not in DEONTICS:
            if len(node.params) == 3:
                self.potential_obl[node.signature].append(node)
            return

        if len(node.params) > 1:
            self.delay_error("Deontic Terms only have a single parameter", node)

        self.deontic_terms[node.params[0].signature].append(node)

    def action_FluentAST(self, visitor, node):
        """
        track obligation fluents
        """
        if node.annotation not in obligations:
            # ignore fluents that aren't obligations
            return

        if len(node.head.params) != 3:
            # Should never actually fire, because the parser catches this
            self.delay_error("An Obligation Fluent doesn't have enough components", node)

        if node.head.signature in self.obligations:
            self.delay_error("Duplicate obligation declared", node)
        else:
            self.obligations[node.head.signature] = node


    def action_EventAST(self, visitor, node):
        if node.annotation not in {iAST.EventEnum.institutional, iAST.EventEnum.violation}:
            return

        self.inst_events[node.head.signature] = node

    def validate(self):
        """
        Ensure that all terms marked with deontic qualifiers,
        are institutional inst_events,
        or obligations
        """
        deontic_terms        = set(self.deontic_terms.keys())
        potential_obls       = set(self.potential_obl.keys())

        inst_event_sigs      = self.inst_events.keys()
        declared_obligations = self.obligations.keys()

        for obl in self.obligations.values():
            # Verify all obligations are made of 3 inst inst_events
            for arg in obl.head.params:
                if arg.signature not in self.inst_events:
                    self.delay_error("Obligation Declared with an incompatiable argument", obl, arg)

            # Verify uses of the obligation match in parameter structure
            for ast in self.potential_obl[obl.head.signature]:
                if not all([x.signature == y.signature for x,y in zip(ast.params, obl.head.params)]):
                    self.delay_error("Obligation Use does not match Declaration", ast)


        # any deontic term not targetting an institutional event is an error
        for term in (deontic_terms - inst_event_sigs):
            for ast in self.deontic_terms[term]:
                self.delay_error("Deontic Qualifier is not applied to an institutional event", ast)
