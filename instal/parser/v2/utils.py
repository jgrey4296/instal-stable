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

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- util
pp.ParserElement.set_default_whitespace_chars(" \t")

s       = pp.Suppress
op      = pp.Optional
orm     = pp.OneOrMore
zrm     = pp.ZeroOrMore
kw      = pp.Keyword
lit     = pp.Literal
gr      = lambda x: pp.Group(x)
s_kw    = lambda x: pp.Keyword(x).suppress()
s_lit   = lambda x: pp.Literal(x).suppress()
ln      = orm(pp.White("\n\r").set_whitespace_chars("\t ")).suppress()
ln.set_name("ln")
comment = pp.Regex(r"%.+?\n")
semi    = s(op(lit(";") | lit(".")) + pp.line_end)
semi.set_name(";")

# TODO: shift these lists into defaults, as dicts to use in constructors as well
event_kws      = pp.MatchFirst(kw(x) for x in ["exogenous", "institutional", "violation", "exo", "inst", "viol", "external"])
fluent_kws     = pp.MatchFirst(kw(x) for x in ["cross", "obligation", "x", "transient", "obl"])
generation_kws = pp.MatchFirst(kw(x) for x in ["generates", "xgenerates"])
inertial_kws   = pp.MatchFirst(kw(x) for x in ["initiates", "terminates", "xinitiates", "xterminates"])
op_lits        = pp.MatchFirst(lit(x) for x in ["<=", ">=", "<>", "!=", "<", ">", "=", ])

not_kw         = kw("not")

at_time = op(s_kw('at') + pp.common.integer('time'))
at_time.set_parse_action(lambda s, l, t: t['time'] if 'time' in t else [0])

##-- end util

##-- term parser
name = pp.Word(pp.alphas.lower() + "_", pp.alphanums + "_")
name.set_parse_action(lambda s, l, t: (False, t[0]))
name.set_name("name")
# TODO: handle explicit type annotation
var       = pp.Word(pp.alphas.upper(), pp.alphanums)
var.set_parse_action(lambda s, l, t: (True, t[0]))
var.set_name("var")

anon_var  = lit("_")
var.set_parse_action(lambda s, l, t: (True, t[0]))
var.set_name("anon_var")

num = pp.common.signed_integer.copy()
num.add_parse_action(lambda s, l, t: (False, t[0]))

# The core Term parser:
TERM      = pp.Forward()
TERM.set_name("term")
term_list = pp.delimited_list(op(ln) + TERM)
term_list.set_name("Term Parameters")

# Number's can't actually be the value, only params,
# but we'll ensure that in a check heuristic
TERM  <<= (var | name | num)("value") + op(lit("(") + term_list("params") + lit(")"))
TERM.set_parse_action(construct.term)
TERM.set_name("term")

in_inst       = s_kw('in') + TERM('inst')
##-- end term parser

##-- conditions
CONDITION   = op(kw("not"))("not") + TERM("head")
CONDITION.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['head'], True if 'not' in t else False, parse_loc=(pp.lineno(l, s), pp.col(l, s))))
CONDITION.set_name("condition")

COMPARISON  = TERM("lhs") + op_lits("op") + TERM("rhs")
COMPARISON.set_parse_action(lambda s, l, t: ASTs.ConditionAST(t['lhs'], False, operator=t['op'], rhs=t['rhs'], parse_loc=(pp.lineno(l, s), pp.col(l, s))))
COMPARISON.set_name("comparison")

CONDITIONS  = pp.delimited_list(op(ln) + (COMPARISON | CONDITION))
CONDITIONS.set_name("Condition list")

if_conds    = op(op(ln) + s_kw("if") + CONDITIONS)

# TODO handle time delay 'in {time}'

##-- end conditions
