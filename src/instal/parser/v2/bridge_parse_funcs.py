#/usr/bin/env python3,
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
import instal.interfaces.ast as ASTs
import instal.parser.v2.constructors as construct
import instal.parser.v2.utils as PU
import instal.parser.v2.institution_parse_funcs as IPF

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- util imports
s       = PU.s
op      = PU.op
orm     = PU.orm
zrm     = PU.zrm
kw      = PU.kw
lit     = PU.lit
gr      = PU.gr
s_kw    = PU.s_kw
s_lit   = PU.s_lit
ln      = PU.ln
comment = PU.comment
semi    = PU.semi

TERM           = PU.TERM
CONDITIONS     = PU.CONDITIONS
term_list      = PU.term_list
event_kws      = PU.event_kws
fluent_kws     = PU.fluent_kws
generation_kws = PU.generation_kws
inertial_kws   = PU.inertial_kws
op_lits        = PU.op_lits

if_conds       = PU.if_conds

##-- end util imports

##-- bridge specific
BRIDGE      = s_kw("bridge") + TERM("head") + semi
BRIDGE.set_parse_action(lambda s, l, t: ASTs.BridgeDefAST(t['head'][0], parse_loc=(pp.lineno(l, s), pp.col(l, s))))

link_kws = pp.MatchFirst([kw(x).set_parse_action(lambda s, l, t: ASTs.BridgeLinkEnum[t[0]]) for x in ASTs.BridgeLinkEnum.__members__.keys()])

BRIDGE_LINK =  link_kws("link_type") + TERM("head") + semi
BRIDGE_LINK.set_parse_action(lambda s, l, t: ASTs.BridgeLinkAST(t['head'], link_type=t['link_type'], parse_loc=(pp.lineno(l, s), pp.col(l, s))))

##-- end bridge specific

##-- top level parser entry points
bridge_structure = (BRIDGE('head')
                    + zrm(BRIDGE_LINK
                          | IPF.TYPE_DEC
                          | IPF.EVENT
                          | IPF.FLUENT
                          | IPF.RULE
                          | IPF.INITIALLY)('body'))

bridge_structure.set_parse_action(construct.institution)
bridge_structure.set_name("Bridge Structure")

top_bridge = orm(bridge_structure + zrm(ln))
top_bridge.ignore(comment)
top_bridge.set_name("Bridges")

##-- end top level parser entry points
