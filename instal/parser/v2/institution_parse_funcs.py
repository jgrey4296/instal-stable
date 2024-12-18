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

##-- rules
GEN_RULE       = (TERM("head")
               + generation_kws("annotation")
               + term_list("body") + if_conds("conditions") + semi)
GEN_RULE.set_parse_action(construct.generate_rule)
GEN_RULE.set_name("event generation rule")

INERTIAL_RULE  = (TERM("head")
               + inertial_kws("annotation")
               + term_list("body") + if_conds("conditions") + semi)
INERTIAL_RULE.set_parse_action(construct.inertial_rule)
INERTIAL_RULE.set_name("inertial fluent rule")

TRANSIENT_RULE  = TERM("body") + s_kw("when") + CONDITIONS("conditions") + semi
TRANSIENT_RULE.set_parse_action(construct.transient_rule)
TRANSIENT_RULE.set_name("transient rule")

RULE = GEN_RULE | INERTIAL_RULE | TRANSIENT_RULE

##-- end rules

##-- types, fluents, events
type_vals = s_lit(":") + orm(TERM)("body")
TYPE_DEC    = s_kw("type") + TERM('head') + op(type_vals) + semi
TYPE_DEC.add_parse_action(lambda s, l, t: ASTs.DomainSpecAST(t['head'], t['body'][:] if 'body' in t else [], parse_loc=(pp.lineno(l, s), pp.col(l, s))))
TYPE_DEC.set_name("type_dec")

FLUENT      = op(fluent_kws)("annotation") + s_kw("fluent") + TERM("head") + semi
FLUENT.set_parse_action(construct.fluent)
FLUENT.set_name("fluent")

EVENT       = event_kws('annotation')  + s_kw("event")  + TERM("head") + semi
EVENT.set_parse_action(construct.event)
EVENT.set_name("event")

INITIALLY   = s_kw("initially") + term_list("body") + if_conds("conditions") + semi
INITIALLY.set_parse_action(lambda s, l, t: ASTs.InitiallyAST(t['body'][:], t.conditions[:], parse_loc=(pp.lineno(l, s), pp.col(l, s))))
INITIALLY.set_name("initially")
##-- end types, fluents, events

##-- institution head
INSTITUTION = s_kw("institution") + TERM("head") + semi
INSTITUTION.set_parse_action(lambda s, l, t: ASTs.InstitutionDefAST(t['head'][0], parse_loc=(pp.lineno(l, s), pp.col(l, s))))
INSTITUTION.set_name("institution head")
##-- end institution head

##-- top level parser entry points
institution_structure = (INSTITUTION('head')
                         + zrm(ln
                               | TYPE_DEC
                               | EVENT
                               | FLUENT
                               | RULE
                               | INITIALLY) ('body'))
institution_structure.set_parse_action(construct.institution)
institution_structure.set_name("Institution Structure")

top_institution = orm(institution_structure + zrm(ln))
top_institution.ignore(comment)
top_institution.set_name("Institutions")

##-- end top level parser entry points
