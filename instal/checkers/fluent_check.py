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
    """ ensure inertial fluents have associated initiation and self.terminations,
    and self.transients don't.
    """

    declarations : dict[iAST.FluentEnum, set[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(set))
    usage        : dict[iAST.RuleEnum,   set[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(set))

    def clear(self):
        self.declarations = defaultdict(set)
        self.usage        = defaultdict(set)

    def get_actions(self):
        return {
            iAST.FluentAST: {self.action_FluentAST},
            iAST.RuleAST  : {self.action_RuleAST}
            }

    def check(self):
        inertials   = self.declarations[iAST.FluentEnum.inertial]
        initiated   = self.usage[iAST.RuleEnum.initiates]
        terminated  = self.usage[iAST.RuleEnum.terminates]

        for fluent in (inertials - initiated):
            self.warning("Inertial Fluent Not Initiated Anywhere", fluent)
        for fluent in (inertials - terminated):
            self.warning("Inertial Fluent Not Terminated Anywhere", fluent)


        transient   = self.declarations[iAST.FluentEnum.transient]
        consequents = self.usage[iAST.RuleEnum.transient]

        for fluent in (transient - consequents):
            self.warning("Transient Fluent Not Mentioned Anywhere", fluent)

        for fluent in (transient & (initiated | terminated)):
            self.error("Transient Fluent treated as an Inertial Fluent", fluent)


    def action_FluentAST(self, visitor, fluent):
        match fluent.annotation:
            case iAST.FluentEnum.inertial | iAST.FluentEnum.transient:
                self.declarations[fluent.annotation].add(fluent.head)

    def action_RuleAST(self, visitor, rule):
        match rule:
            case iAST.RuleAST(annotation=iAST.RuleEnum.initiates):
                self.usage[rule.annotation].update(rule.body)
            case iAST.RuleAST(annotation=iAST.RuleEnum.terminates):
                self.usage[rule.annotation].update(rule.body)
            case iAST.RuleAST(annotation=iAST.RuleEnum.transient):
                self.usage[rule.annotation].add(rule.head)
