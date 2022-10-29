##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)

from instal.interfaces.checker import InstalChecker_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class EventCheck(InstalChecker_i):
    """ check external events generate institutional events

    Uses a basic pair of sets to track all defined external and institutional events,
    then removes external events when they are used in heads of generation rules,
    and removes institutional events when they are used in bodies of generation rules.

    Could be improved to track generation in a graph, and detect cycles/islands
    """

    def check(self, asts):
        ex_events = set()
        in_events = set()

        ##-- loop over everything, record declarations and uses
        for ast in asts:
            if not isinstance(ast, iAST.InstitutionDefAST):
                continue

            for event in ast.events:
                match event.annotation:
                    case iAST.EventEnum.exogenous if isinstance(ast, iAST.BridgeDefAST):
                        self.warning("Bridge Institutions should not have external events")
                    case iAST.EventEnum.exogenous:
                        ex_events.add(event.head)
                    case iAST.EventEnum.institutional:
                        in_events.add(event.head)
                    case _:
                        pass

            for rule in ast.rules:
                if not isinstance(rule, iAST.GenerationRuleAST):
                    continue

                ex_events.discard(rule.head)
                in_events.difference_update(rule.body)

        ##-- end loop over everything, record declarations and uses

        ##-- if anything remains: report it
        for ex_event in ex_events:
            self.warning("Unused External Event", ex_event)

        for in_event in in_events:
            self.warning("Non-Generated Institutional Event", in_event)

        ##-- end if anything remains: report it
