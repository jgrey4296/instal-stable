##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from itertools import combinations

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class NameDuplicationValidator(InstalValidator_i):
    """" warn on event/fluent/typedec name duplication

    The `action_X` methods are called as the ast is visited, for basic duplications.
    when everything is finished, conflicts are detected by `validator`
    """

    events   : dict[str, list[iAST.EventAST]]      = field(init=False, default_factory=lambda: defaultdict(list))
    fluents  : dict[str, list[iAST.FluentAST]]     = field(init=False, default_factory=lambda: defaultdict(list))
    typeDecs : dict[str, list[iAST.DomainSpecAST]] = field(init=False, default_factory=lambda: defaultdict(list))

    def validate(self):
        for lhs, rhs in combinations([self.events, self.fluents, self.typeDecs], 2):
            lhs_sigs = set(lhs.keys())
            rhs_sigs = set(rhs.keys())

            for sig in (lhs_sigs & rhs_sigs):
                lhs_val = lhs[sig][0]
                rhs_val = rhs[sig][0]
                self.error("Declaration Conflict", lhs_val, rhs_val)

    def action_EventAST(self, visitor, event):
        if event.head.signature in self.events:
            self.error(f"Duplicate Event Declaration", event)
        else:
            self.events[event.head.signature].append(event)

    def action_FluentAST(self, visitor, fluent):
        if fluent.head.signature in self.fluents:
            self.error(f"Duplicate Fluent Declaration", fluent)
        else:
            self.fluents[fluent.head.signature].append(fluent)


    def action_DomainSpecAST(self, visitor, typeDec):
        if typeDec.head.signature in self.typeDecs:
            self.error(f"Duplicate TypeDec Declaration", typeDec)
        else:
            self.typeDecs[typeDec.head.signature].append(typeDec)
