##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class QueryValidator(InstalValidator_i):
    """ ensure queries are of defined external events """

    queries : dict[str, list[iAST.QueryAST]] = field(init=False, default_factory=lambda: defaultdict(list))
    events  : dict[str, list[iAST.EventAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def action_QueryAST(self, visitor, node):
        self.queries[node.head.signature].append(node)

    def action_EventAST(self, visitor, node):
        if node.annotation is iAST.EventEnum.exogenous:
            self.events[node.head.signature].append(node)


    def validate(self):
        undefined_events = set(self.queries.keys()) - self.events.keys()

        for sig in undefined_events:
            for query in self.queries[sig]:
                self.delay_error("Undeclared Event used in Query", query)
