#/usr/bin/env python3,
""",
,
""",
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

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- consts
comparisons = ["==", "!=", "<" ">" "<=", ">="]
##-- end consts

##-- util
s         = pp.Suppress
op        = pp.Optional
orm       = pp.OneOrMore
zrm       = pp.ZeroOrMore
kw        = pp.Keyword
lit       = pp.Literal
##-- end util


comment    = pp.Regex(r"%.+?")
semi       = lit(";")
fluent_kws = [kw(x) for x in ["cross", "noninertial", "obligation"]]
event_kws  = [kw(x) for x in ["exogenous", "inst", "violation"]]

name = pp.Word(pp.alphanums)
var  = pp.Word(pp.alphas.upper(), pp.alphanums)

term      = pp.Forward()
term_list = pp.delimited_list(term)

term  <<= name + op(lit("(") + term_list + lit(")"))

type_dec    = kw("type") + term + semi
domain_spec = name + lit(":") + orm(name)

fluent = op(pp.MatchFirst(fluent_kws)) + kw("fluent") + term + semi
event  = op(pp.MatchFirst(event_kws))  + kw("event")  + term + semi

condition = pp.Empty()
relation  = (term
             + pp.MatchFirst([kw(x) for x in ["generates", "initiates", "terminates",
                                              "xgenerates", "xinitiates", "xterminates"]])
             + term_list + op(condition) + semi)

obligation = term + kw("when") + term_list + semi
initially = kw("initially")    + term_list + semi

bridge = kw("bridge") + term + semi
sink   = kw("sink") + term + semi
source = kw("source") + term + semi


parse_point = None
