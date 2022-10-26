##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i

##-- end imports

@dataclass
class RuleCheck(InstalChecker_i):
    """ check rules make sense

    generation rules : only events generate states

    initial rules    : only initiate states

    initiate rules   : only institutional events start states
    terminate rules  : only institutional events end states

    transient rules  : only states set transient state
    """

    def check(self, ast):
        pass
