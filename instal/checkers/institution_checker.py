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
class InstitutionChecker(InstalChecker_i):

    def check(self, ast):
        self.check_head(ast)

    def occurs(self, whens):
        def update_occurs_graph(whengraph, lhs, w):
            if w[0] == "and":
                update_occurs_graph(whengraph, lhs, w[1])
                update_occurs_graph(whengraph, lhs, w[2])
            elif w[0] in self.EXPR_SYMBOLS:
                return
            elif w[0] == "not":
                update_occurs_graph(whengraph, lhs, w[1])
            else:
                whengraph.add_edge(lhs[0], w[0])
        whengraph = networkx.DiGraph()
        for w in whens:
            update_occurs_graph(whengraph, w[0],  w[1])
        if next(networkx.simple_cycles(whengraph),None) is not None:
            raise InstalParserTypeError("Failed occurs check (this means there are cyclical references in your when norms.)")

    ##-- end misc
