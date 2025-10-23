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
class BridgeFluentGenValidator(InstalValidator_i):
    """
    Validator cross institution fluent generation connections
    """

    def action_BridgeDefAST(self, visitor, node):
        assert(isinstance(node, iAST.BridgeDefAST))
        bridge_insts.update({x.head.signature for x in node.links})
        # record cross generation fluents
        for rule in node.rules:
            if rule.annotation not in {iAST.RuleEnum.xinitiates, iAST.RuleEnum.xterminates}:
                continue

            bridge_fluents[rule.head.signature] = rule
            bridge_fluents.update({x.signature: rule for x in rule.body})



    def action_InstitutionDefAST(self, visitor, node):
        assert(isinstance(node, iAST.InstitutionDefAST))
        # record institutional fluents
        for fluent in node.fluents:
            if fluent.annotation is not iAST.FluentEnum.cross:
                continue

            inst_fluents[node.head.signature][fluent.head.signature] = fluent


    def validate(self):
        bridge_fluents = {}
        bridge_insts   = set()
        inst_fluents   = defaultdict(dict)


        # verify all cross generation
        missing_fluents = set(bridge_fluents.keys())
        for sig in bridge_insts.intersection(inst_fluents.keys()):
            inst_keys = inst_fluents[sig].keys()
            missing_fluents.difference_update(inst_keys)

        for sig in missing_fluents:
            rule = bridge_fluents[sig]
            self.delay_error("Undeclared fluent used in bridge", rule)
