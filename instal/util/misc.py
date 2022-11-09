
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
            return maybe_path.read_text(), str(maybe_path)
        case _:
            raise TypeException("Unknown type used in parser", maybe_path)
