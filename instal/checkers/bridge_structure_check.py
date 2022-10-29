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
        sources      = dict()
        sinks        = dict()
        institutions = set()

        ##-- loop all institutions: record sources and sinks
        for ast in asts:
            if not isinstance(ast, iAST.InstitutionDefAST):
                continue

            institutions.add(ast.head.signature)

            if not isinstance(ast, iAST.BridgeDefAST):
                continue

            sources.update({x.signature: x for x in ast.sources})
            sinks.update({x.signature: x for x in ast.sinks})

            if not bool(ast.sources):
                self.warning("Bridge has no sources", ast)

            if not bool(ast.sinks):
                self.warning("Bridge has not sinks", ast)

        ##-- end loop all institutions: record sources and sinks

        ##-- report sources/sinks that arent defined
        missing_sources = {y for x,y in sources.items() if x not in institutions}
        missing_sinks   = {y for x,y in sinks.items()   if x not in institutions}

        for source in missing_sources:
            self.warning("Bridge Source declared but not defined", source)

        for sink in missing_sinks:
            self.warning("Bridge Sink declared but not defined", sink)

        ##-- end report sources/sinks that arent defined
