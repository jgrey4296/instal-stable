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
class NameDuplicationCheck(InstalChecker_i):

    def check(self, ast):
        # TODO: warn on event/fluent name duplication
        pass


    ##-- end misc
