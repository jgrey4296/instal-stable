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
class FluentValidator(InstalValidator_i):
    """ ensure inertial fluents have associated initiation and self.terminations,
    and self.transients don't.
    """

    declarations : dict[iAST.FluentEnum, set[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(set))
    usage        : dict[iAST.RuleEnum,   set[iAST.TermAST]] = field(init=False, default_factory=lambda: defaultdict(set))


    def validate(self):
        inertials   = self.declarations[iAST.FluentEnum.inertial]
        initiated   = self.usage[iAST.RuleEnum.initiates]
        terminated  = self.usage[iAST.RuleEnum.terminates]

        for fluent in (inertials - initiated):
            self.delay_warning("Inertial Fluent Not Initiated Anywhere", fluent)
        for fluent in (inertials - terminated):
            self.delay_warning("Inertial Fluent Not Terminated Anywhere", fluent)


        transient   = self.declarations[iAST.FluentEnum.transient]
        consequents = self.usage[iAST.RuleEnum.transient]

        for fluent in (transient - consequents):
            self.delay_warning("Transient Fluent Not Mentioned Anywhere", fluent)

        for fluent in (transient & (initiated | terminated)):
            self.delay_error("Transient Fluent treated as an Inertial Fluent", fluent)


    def action_FluentAST(self, visitor, fluent):
        match fluent.annotation:
            case iAST.FluentEnum.inertial | iAST.FluentEnum.transient:
                self.declarations[fluent.annotation].add(fluent.head)

    def action_InertialRuleAST(self, visitor, rule):
        match rule:
            case iAST.RuleAST(annotation=iAST.RuleEnum.initiates):
                self.usage[rule.annotation].update(rule.body)
            case iAST.RuleAST(annotation=iAST.RuleEnum.terminates):
                self.usage[rule.annotation].update(rule.body)

    def action_TransientRuleAST(self, visitor, rule):
        assert(rule.annotation == iAST.RuleEnum.transient)
        self.usage[rule.annotation].add(rule.head)
