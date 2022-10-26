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
class FluentCheck(InstalChecker_i):
    """ ensure inertial fluents have associated initiation and terminations,
    and transients don't.
    """

    def check(self, ast):

        pass
