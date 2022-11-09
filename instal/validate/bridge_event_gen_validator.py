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
class BridgeEventGenValidator(InstalValidator_i):
    """
    Validator cross institution event generation connections
    """

    bridge_events : dict[str, iAST.RuleAST]             = field(init=False, default_factory=dict)
    bridge_insts  : set[str]                            = field(init=False, default_factory=set)
    inst_events   : dict[str, dict[str, iAST.EventAST]] = field(init=False, default_factory=lambda: defaultdict(dict))

    def action_BridgeDefAST(self, visitor, node):
        """
        track cross generation events in bridge
        """
        assert(isinstance(node, iAST.BridgeDefAST))
        self.bridge_insts.update({x.head.signature for x in node.links})

        # record cross generation events
        for rule in node.rules:
            if rule.annotation is not iAST.RuleEnum.xgenerates:
                # ignore non-cross generates
                continue

            self.bridge_events[rule.head.signature] = rule
            self.bridge_events.update({x.signature: rule for x in rule.body})


    def action_InstitutionDefAST(self, visitor, node):
        """
        track institutional events in normal insts
        """
        assert(isinstance(node, iAST.InstitutionDefAST))
        # record institutional events
        for event in node.events:
            if event.annotation is not iAST.EventEnum.institutional:
                # ignore externals
                continue

            self.inst_events[node.head.signature][event.head.signature] = event


    def validate(self):
        """
        with all events tracked, make sure they line up
        """
        # verify all cross generation
        missing_events = set(self.bridge_events.keys())
        for sig in self.bridge_insts.intersection(self.inst_events.keys()):
            inst_keys = self.inst_events[sig].keys()
            missing_events.difference_update(inst_keys)

        for sig in missing_events:
            rule = self.bridge_events[sig]
            self.delay_error("Undeclared institutional event used in bridge", rule)
