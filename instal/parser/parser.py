#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import pyparsing as pp
from instal.interfaces.parser import InstalParser_i
import instal.interfaces.ast as ASTs
import instal.parser.parse_funcs as PF

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- interface implementation
class InstalPyParser(InstalParser_i):

    def parse_institution(self, text:str, *, source:str=None) -> ASTs.InstitutionDefAST:
        """ Mainly for .ial's """
        result = PF.top_institution.parse_string(text, parse_all=True)[0]
        if source is not None:
            result.source = source
        return result

    def parse_bridge(self, text:str, *, source:str=None) -> ASTs.BridgeDefAST:
        """ Mainly for .iab's """
        result = PF.top_bridge.parse_string(text, parse_all=True)[0]
        if source is not None:
            result.source = source
        return result

    def parse_domain(self, text:str, *, source:str=None) -> ASTs.DomainTotalityAST:
        """ For .idc's """
        result = PF.top_domain.parse_string(text, parse_all=True)[0]
        if source is not None:
            result.source = source
        return result

    def parse_situation(self, text:str, *, source:str=None) -> ASTs.FactTotalityAST:
        """ Mainly for .iaf's """
        result = PF.top_fact.parse_string(text, parse_all=True)[0]
        if source is not None:
            result.source = source
        return result

    def parse_query(self, text:str, *, source:str=None) -> ASTs.QueryTotalityAST:
        """ Mainly for .iaq's """
        result = PF.top_query.parse_string(text, parse_all=True)[0]
        if source is not None:
            result.source = source
        return result

##-- end interface implementation
