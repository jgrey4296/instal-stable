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
class EventValidator(InstalValidator_i):
    """ validator external events generate institutional events

    Uses a basic pair of sets to track all defined external and institutional events,
    then removes external events when they are used in heads of generation rules,
    and removes institutional events when they are used in bodies of generation rules.

    Could be improved to track generation in a graph, and detect cycles/islands
    """

    declarations : dict[iAST.EventEnum, set[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(set))
    usage        : set[iAST.TermAST]                       = field(init=False, default_factory=set)

    def validate(self):
        for event in (self.declarations[iAST.EventEnum.exogenous] - self.usage):
            self.delay_warning("Unused External Event", event)

        for event in (self.declarations[iAST.EventEnum.institutional] - self.usage):
            self.delay_warning("Institutional Event is not generated", event)

    def action_EventAST(self, visitor, event):
        match event.annotation:
            case iAST.EventEnum.exogenous | iAST.EventEnum.institutional:
                self.declarations[event.annotation].add(event.head)
            case _:
                pass

    def action_GenerationRuleAST(self, visitor, rule):
        self.usage.add(rule.head)
        self.usage.update(rule.body)
