##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.validate import InstalValidator_i
from instal.interfaces import ast as iAST

##-- end imports

@dataclass
class BridgeStructureValidator(InstalValidator_i):
    """ Validator bridges have sources and sinks,
    and those sources and sinks are defined
    """

    sources      = dict()
    sinks        = dict()
    institutions = set()


    def action_InstitutionDefAST(self, visitor, ast):
        self.institutions.add(ast.head.signature)

    def action_BridgeDefAST(self, visitor, ast):
        self.sources.update({x.head.signature: x for x in ast.links if x.link_type is iAST.BridgeLinkEnum.source})
        self.sinks.update({x.head.signature: x for x in ast.links if x.link_type is iAST.BridgeLinkEnum.sink})

        if not bool(ast.links):
            self.delay_warning("Bridge has no links", ast)


    def validate(self):
        ##-- report sources/sinks that arent defined
        missing_sources = [y for x,y in self.sources.items() if x not in self.institutions]
        missing_sinks   = [y for x,y in self.sinks.items()   if x not in self.institutions]

        for source in missing_sources:
            self.delay_warning("Bridge Source declared but not defined", source)

        for sink in missing_sinks:
            self.delay_warning("Bridge Sink declared but not defined", sink)

        ##-- end report sources/sinks that arent defined
