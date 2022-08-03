
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

from instal import defaults
##-- end imports

logging = logmod.getLogger(__name__)

InstalFile = NewType("InstalFile",_io._TextIOBase)

@dataclass
class InstalFileGroup:
    institutions : list[Path] = field(default_factory=list)
    bridges      : list[Path] = field(default_factory=list)
    domains      : list[Path] = field(default_factory=list)
    situation    : list[Path] = field(default_factory=list)
    compiled     : list[Path] = field(default_factory=list)
    query        : None|Path  = field(default=None)

    @staticmethod
    def from_targets(*targets):
        """
        Take directories and files, and create the file group
        """
        queue = [Path(x) for x in targets]
        found = set()
        file_group = InstalFileGroup()
        while bool(queue):
            target = queue.pop()
            if not target.exists():
                logging.warning("Specified target does not exist: %s", target)
            elif target.is_dir():
                queue += [x for x in target.iterdir()]
            elif target.is_file():
                match target.suffix:
                    case defaults.COMPILED_EXT:
                        file_group.compiled.append(target)
                    case defaults.INST_EXT:
                        file_group.institutions.append(target)
                    case defaults.BRIDGE_EXT:
                        file_group.bridges.append(target)
                    case defaults.SITUATION_EXT:
                        file_group.situation.append(target)
                    case defaults.DOMAIN_EXT:
                        file_group.domains.append(target)
                    case defaults.QUERY_EXT if file_group.query is None:
                        file_group.query = target
                    case defaults.QUERY_EXT:
                        logging.warning("Multiple Queries found, ignoring: %s", target)
                    case _:
                        logging.warning("Unrecognized file type found: %s", target)

        return file_group




    def __len__(self):
        return (len(self.institutions)
                + len(self.bridges)
                + len(self.domains)
                + len(self.situation)
                + len(self.compiled)
                + (1 if self.query is not None else 0))

@dataclass
class InstalOptionGroup:
    verbose    : int       = field(default=0)
    answer_set : int       = field(default=0)
    length     : int       = field(default=1)
    number     : int       = field(default=1)

    output     : None|Path = field(default=None)
    json       : bool      = field(default=False)
    gantt      : bool      = field(default=False)
    text       : bool      = field(default=True)
    trace      : Any       = field(default=None)

    def __post_init__(self):
        # set the log verbosity,
        # create output dir's as necessary
        instal_root = logmod.getLogger("instal")
        instal_root.setLevel(max(logmod.DEBUG, logmod.ERROR - (10 * self.verbose)))
        print("Logging Level Set to: %s", logmod.getLevelName(instal_root.level))

        if self.output is None:
            logging.warning("No Output directory specified")
        else:
            assert(self.output.is_dir())
            if not self.output.exists():
                logging.info("Making Output Directory: %s", self.output)
                self.output.mkdir(parents=True)

            assert(self.json or self.gantt or self.text), "No Output option selected"


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

