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
class QueryValidator(InstalValidator_i):
    """ ensure queries are of defined external events """

    def validate(self):

        pass
