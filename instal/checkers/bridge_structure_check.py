##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class BridgeStructureChecker(InstalChecker_i):
    """ Check bridges have sources and sinks,
    and those sources and sinks are defined
    """

    def check(self, asts):
        sources = set()
        sinks   = set()
        institutions   = set()

        ##-- loop all institutions: record sources and sinks
        for ast in asts:
            if not isinstance(ast, iAST.InstitutionDefAST):
                pass

            institutions.add(ast.head)

            if not isinstance(ast, iAST.BridgeDefAST):
                pass

            sources.update(ast.sources)
            sinks.update(ast.sinks)

            if not bool(ast.sources):
                self.warning("Bridge has no sources", ast)

            if not bool(ast.sinks):
                self.warning("Bridge has not sinks", ast)

        ##-- end loop all institutions: record sources and sinks

        ##-- report sources/sinks that arent defined
        missing_sources = {x for x in sources if x not in institutions}
        missing_sinks   = {x for x in sinks   if x not in institutions}

        if bool(missing_sources):
            self.warning("Bridge Sources were declared but not defined", missing_sources)

        if bool(missing_sinks):
            self.warning("Bridge Sinks were declared but not defined", missing_sinks)

        ##-- end report sources/sinks that arent defined
