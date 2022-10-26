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
class TermDeclarationCheck(InstalChecker_i):
    """ Check all terms are declared, and use consistent number of arguments
    check no term starts with a number,
    and no Variable has params
    """

    def check(self, asts):
        self.check_term_declared(asts)
        self.check_term_args(asts)

    def check_term_declared(self):
        # TODO Check term has been declared as an event/fluent
        pass

    def check_term_args(self):
        # TODO check a term has the right number of arguments as declared
        pass
