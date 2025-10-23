
##-- imports
from __future__ import annotations

import pathlib as pl
import logging as logmod
from dataclasses import InitVar, dataclass, field
from typing import NewType

from instal import defaults
##-- end imports

logging = logmod.getLogger(__name__)

def maybe_read_path(maybe_path:str|pl.Path, parse_source) -> tuple[str, str]:
    """
    a simple utility for parsing,
    reading a path if necessary,
    and returning a text and its source
    """
    match maybe_path, parse_source:
        case str(), _:
            return maybe_path, parse_source
        case pl.Path(), _:
            return maybe_path.read_text(), maybe_path
        case _:
            raise TypeException("Unknown type used in parser", maybe_path)

def maybe_get_query_and_situation(query:None|str, situation:None|str) -> tuple[list[TermAST], list[TermAST]]:
    """
    Try to parse a query and situation specification,
    without erroring if no targets are provided

    Returns a tuple of lists of TermASTs, which are empty if the targets produce nothing
    """
    from instal.parser.parser import InstalPyParser
    parser    = InstalPyParser()
    situation = []
    query     = []

    if situation:
        as_path    = pathlib.Path(situation).expanduser().resolve()
        parse_this = as_path if as_path.exists() else situation.replace("\\n", "\n")
        situation += parser.parse_situation(parse_this).body[:]

    if query:
        as_path    = pathlib.Path(query).expanduser().resolve()
        parse_this = as_path if as_path.exists() else query.replace("\\n", "\n")
        query     += parser.parse_query(parse_this).body[:]


    return query, situation
