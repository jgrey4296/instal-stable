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
class BridgeFluentGenCheck(InstalChecker_i):
    """
    Check cross institution fluent generation connections
    """

    def check(self, asts):
        bridge_fluents = {}
        bridge_insts   = set()
        inst_fluents   = defaultdict(dict)

        ##-- accumulate
        for ast in asts:
            match ast:
                case iAST.BridgeDefAST():
                    bridge_insts.update({x.signature for x in ast.sources})
                    bridge_insts.update({x.signature for x in ast.sinks})
                    # record cross generation fluents
                    for rule in ast.rules:
                        if rule.annotation not in {iAST.RuleEnum.xinitiates, iAST.RuleEnum.xterminates}:
                            continue

                        bridge_fluents[rule.head.signature] = rule
                        bridge_fluents.update({x.signature: rule for x in rule.body})


                case iAST.InstitutionDefAST():
                    # record institutional fluents
                    for fluent in ast.fluents:
                        if fluent.annotation is not iAST.FluentEnum.cross:
                            continue

                        inst_fluents[ast.head.signature][fluent.head.signature] = fluent

        ##-- end accumulate

        # verify all cross generation
        missing_fluents = set(bridge_fluents.keys())
        for sig in bridge_insts.intersection(inst_fluents.keys()):
            inst_keys = inst_fluents[sig].keys()
            missing_fluents.difference_update(inst_keys)

        for sig in missing_fluents:
            rule = bridge_fluents[sig]
            self.error("Undeclared fluent used in bridge", rule)
