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
class FluentCheck(InstalChecker_i):
    """ ensure inertial fluents have associated initiation and terminations,
    and transients don't.
    """

    def check(self, asts):
        initiations  = set()
        terminations = set()
        transients   = set()

        ##-- loop asts and record what exists/is used
        for ast in asts:
            if not isinstance(ast, iAST.InstitutionDefAST):
                continue

            for fluent in ast.fluents:
                match fluent.annotation:
                    case iAST.FluentEnum.inertial:
                        initiations.add(fluent.head)
                        terminations.add(fluent.head)
                    case iAST.FluentEnum.transient:
                        transients.add(fluent.head)

            for rule in ast.rules:
                match rule:
                    case iAST.InertialRuleAST(annotation=iAST.RuleEnum.initiates):
                        initiations.difference_update(rule.body)
                    case iAST.InertialRuleAST(annotation=iAST.RuleEnum.terminates):
                        terminations.difference_update(rule.body)
                    case iAST.TransientRuleAST(annotation=iAST.RuleEnum.transient):
                        transients.discard(rule.head)

        ##-- end loop asts and record what exists/is used


        ##-- if anything remains: report it
        for x in initiations:
            self.warning("Non-Initiated Inertial Fluent", x)

        for x in terminations:
            self.warning("Non-Terminated Inertial Fluent", x)

        for x in transients:
            self.warning("Unmentioned Transient Fluent", x)

        ##-- end if anything remains: report it
