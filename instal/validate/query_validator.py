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
        pass

    def action_EventAST(self, visitor, node):
        pass


    def validate(self):

        pass
