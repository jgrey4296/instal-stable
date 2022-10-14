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

##-- idc domain
DOMAIN_SPEC = PU.TERM('head') + PU.s_lit(":") + PU.orm(PU.TERM)("body") + pp.line_end
DOMAIN_SPEC.set_parse_action(lambda s, l, t: ASTs.DomainSpecAST(t['head'], t['body'][:]))

top_domain = PU.orm(DOMAIN_SPEC)
top_domain.ignore(PU.comment)
top_domain.set_name("Domain Specifications")
##-- end idc domain

##-- iaf facts / situation
if_conds      = PU.if_conds
IAF_INITIALLY = PU.op(PU.not_kw("not")) + PU.s_kw("initially") + PU.TERM("body") + PU.in_inst + if_conds + pp.line_end
IAF_INITIALLY.set_parse_action(lambda s, l, t: ASTs.InitiallyAST([t['body']],
                                                                 conditions=t.conditions[:],
                                                                 inst=t['inst'],
                                                                 negated='not' in t))
IAF_INITIALLY.add_condition(lambda s, l, t: not any(x.has_var for x in t[0].body))

top_fact = PU.orm(IAF_INITIALLY)
top_fact.ignore(PU.comment)
top_fact.set_name("Initial Facts")
##-- end iaf facts / situation

##-- iaq query specification
OBSERVED = PU.op(PU.not_kw("not")) + PU.s_kw('observed') + PU.TERM('fact') + PU.at_time('time') + if_conds('conds') + PU.semi
OBSERVED.set_parse_action(lambda s, l, t: ASTs.QueryAST(t['fact'],
                                                        time=t.time[0],
                                                        negated='not' in t,
                                                        conditions=t['conds'][:] if 'conds' in t else []))

top_query = PU.orm(OBSERVED)
top_query.ignore(PU.comment)
top_query.set_name("Queries")
##-- end iaq query specification
