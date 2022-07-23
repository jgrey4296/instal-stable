
##-- imports
from __future__ import annotations

from pathlib import Path
import hashlib
import logging as logmod
from dataclasses import InitVar, dataclass, field
from tempfile import NamedTemporaryFile
from typing import NewType

import _io
from clingo import Function, Symbol
##-- end imports

logging = logmod.getLogger(__name__)

InstalFile = NewType("InstalFile",_io._TextIOBase)

@dataclass
class InstalFileGroup:
    files : InitVar[list[str]] = None

    institutions : list[Path] = field(default_factory=list)
    bridges      : list[Path] = field(default_factory=list)
    compiled     : list[Path] = field(default_factory=list)
    domains      : list[Path] = field(default_factory=list)
    facts        : list[Path] = field(default_factory=list)
    query        : None|Path  = field(default=None)

    def __post_init__(self, files):
        # TODO get files from directories,
        # and put them in the right field
        pass

@dataclass
class InstalOptionGroup:
    verbose    : int = field(default=0)
    answer_set : int = field(default=0)
    length     : int = field(default=1)
    number     : int = field(default=1)

    output     : None|Path = field(default=None)
    json_out   : None|Path = field(default=None)
    gantt_out  : None|Path = field(default=None)
    text_out   : None|Path = field(default=None)
    trace      : Any = field(default=None)

    def __post_init__(self):
        # set the log verbosity,
        # create output dir's as necessary


# ############################################################################
def temporary_text_file(text="", file_extension="", delete=True) -> "File":
    """Returns a NamedTemporaryFile with the specified file extension and prints text to it."""
    tmpfile = NamedTemporaryFile(suffix=file_extension, mode="w+t", delete=delete)
    print(text, file=tmpfile)
    return tmpfile


def fun_to_asp(fun: Function) -> str:
    """Takes a gringo fun object and returns what it is in ASP."""
    if isinstance(fun, Symbol):
        return str(fun) + ".\n"
    return ""

def encode_Fun(obj: Symbol) -> dict:
    return {"__Fun__": True, "name": obj.name, "args": obj.arguments}

