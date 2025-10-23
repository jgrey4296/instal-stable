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
class BridgeDeonticsValidator(InstalValidator_i):
    """ validator bridge deontics are consistent """

    def validate(self):
        pass
