##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i

##-- end imports

@dataclass
class RuleValidator(InstalValidator_i):
    """ ensure rules make sense

    generation rules : only events generate states

    initial rules    : only initiate states

    initiate rules   : only institutional events start states
    terminate rules  : only institutional events end states

    transient rules  : only states set transient state
    """

    def validate(self):
        pass
