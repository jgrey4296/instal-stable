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
class BridgeEventGenCheck(InstalChecker_i):
    """
    Check cross institution event generation connections
    """

    def check(self, asts):

        bridge_events = {}
        bridge_insts  = set()
        inst_events   = defaultdict(dict)

        ##-- accumulate
        for ast in asts:
            match ast:
                case iAST.BridgeDefAST():
                    bridge_insts.update({x.head.signature for x in ast.links})
                    # record cross generation events
                    for rule in ast.rules:
                        if rule.annotation is not iAST.RuleEnum.xgenerates:
                            continue

                        bridge_events[rule.head.signature] = rule
                        bridge_events.update({x.signature: rule for x in rule.body})


                case iAST.InstitutionDefAST():
                    # record institutional events
                    for event in ast.events:
                        if event.annotation is not iAST.EventEnum.institutional:
                            continue

                        inst_events[ast.head.signature][event.head.signature] = event

        ##-- end accumulate

        # verify all cross generation
        missing_events = set(bridge_events.keys())
        for sig in bridge_insts.intersection(inst_events.keys()):
            inst_keys = inst_events[sig].keys()
            missing_events.difference_update(inst_keys)

        for sig in missing_events:
            rule = bridge_events[sig]
            self.error("Undeclared institutional event used in bridge", rule)
