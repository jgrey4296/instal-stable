##-- imports
from __future__ import annotations

from importlib.resources import files
import abc
import logging as logmod
import os
from string import Template
from dataclasses import InitVar, dataclass, field
from pathlib import Path

from instal.interfaces import ast as ASTs
from instal.defaults import STANDARD_PRELUDE_loc, DATA_loc

##-- end imports

logging = logmod.getLogger(__name__)

##-- data
try:
    inst_prelude = files(STANDARD_PRELUDE_loc)
except ModuleNotFoundError:
    data = files(DATA_loc)
    inst_prelude = data / STANDARD_PRELUDE_loc

##-- end data

class InstalCompiler_i(metaclass=abc.ABCMeta):
    """
    Interface for compiling InstaASTR down to a
    specific solver format
    """
    def __init__(self):
        self._compiled_text : list[str] = []

    def clear(self):
        self._compiled_text = []


    def insert(self, pattern:str|Template, **kwargs):
        """
        insert a given pattern text into the compiled output,
        formatting it with kwargs.
        """
        match pattern:
            case Template():
                self._compiled_text.append(pattern.safe_substitute(kwargs))
            case str() if not bool(kwargs):
                self._compiled_text.append(pattern)
            case str():
                self._compiled_text.append(pattern.format_map(kwargs))
            case _:
                raise TypeError("Unrecognised compile pattern type", pattern)

    def _load_prelude(self) -> str:
        text = []
        if inst_prelude.is_dir():
            for path in sorted(inst_prelude.iterdir()):
                text += path.read_text().split("\n")
        else:
            assert(inst_prelude.is_file())
            text.append(inst_prelude.read_text())

        text.append("%% End of Prelude")

        return "\n".join(text)

    @abc.abstractmethod
    def compile(self, data:ASTs.InstalAST) -> str: pass
