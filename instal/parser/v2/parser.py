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
import instal.parser.v2.parse_funcs as PF

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- interface implementation
class InstalPyParser(InstalParser_i):

    def parse_institution(self, text:str, *, parse_source:str=None) -> list[ASTs.InstitutionDefAST]:
        """ Mainly for .ial's """
        logging.debug("Parsing Institution, parse_source: %s", parse_source)
        result = PF.top_institution.parse_string(text, parse_all=True)[:]
        if parse_source is not None:
            [x.parse_source.append(parse_source) for x in result]
        return result

    def parse_bridge(self, text:str, *, parse_source:str=None) -> list[ASTs.BridgeDefAST]:
        """ Mainly for .iab's """
        logging.debug("Parsing Bridge, parse_source: %s", parse_source)
        result = PF.top_bridge.parse_string(text, parse_all=True)[:]
        if parse_source is not None:
            [x.parse_source.append(parse_source) for x in result]
        return result

    def parse_domain(self, text:str, *, parse_source:str=None) -> list[ASTs.DomainSpecAST]:
        """ For .idc's """
        logging.debug("Parsing Domain, parse_source: %s", parse_source)
        result = PF.top_domain.parse_string(text, parse_all=True)[:]
        if parse_source is not None:
            [x.parse_source.append(parse_source) for x in result]
        return result

    def parse_situation(self, text:str, *, parse_source:str=None) -> list[ASTs.InitiallyAST]:
        """ Mainly for .iaf's """
        logging.debug("Parsing Situation, parse_source: %s", parse_source)
        result = PF.top_fact.parse_string(text, parse_all=True)[:]
        if parse_source is not None:
            [x.parse_source.append(parse_source) for x in result]
        return result

    def parse_query(self, text:str, *, parse_source:str=None) -> list[ASTs.QueryAST]:
        """ Mainly for .iaq's """
        logging.debug("Parsing Query, parse_source: %s", parse_source)
        result = PF.top_query.parse_string(text, parse_all=True)[:]
        if parse_source is not None:
            [x.parse_source.append(parse_source) for x in result]
        return result

##-- end interface implementation
