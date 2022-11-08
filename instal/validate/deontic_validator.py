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
class DeonticValidator(InstalValidator_i):
    """ validator perm/pow/obl/viol only apply to institutional events """

    def validate(self):

        pass
