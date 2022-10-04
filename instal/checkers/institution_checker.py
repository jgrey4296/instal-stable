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


    def check_head(self, ast):
        if str(ast.head) == "":
            self.error("No Name declared for institution")

    def check_declaration_name_duplicates(self):
        # TODO: warn on event/fluent name duplication
        pass

    def check_declaration_types(self):
        # TODO check variables match declared types
        pass


    def check_term_declared(self):
        # TODO Check term has been declared as an event/fluent
        pass

    def check_term_args(self):
        # TODO check a term has the right number of arguments as declared
        pass


    def check_deontics(self):
        # TODO check perm/pow/obl/viol only apply to institutional events
        pass
    def check_events(self):
        # TODO check ex events generate inst events
        pass

    def check_names(self):
        # TODO Check declared events/fluents are valid in clingo
        pass


    def check_conditions(self):
        pass
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
