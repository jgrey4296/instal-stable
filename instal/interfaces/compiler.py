##-- imports
from __future__ import annotations

import abc
import logging as logmod
import os
from string import Template
import pathlib
from dataclasses import InitVar, dataclass, field
from pathlib import Path

from instal.interfaces import ast as ASTs
from instal.util.misc import temporary_text_file

##-- end imports

logging = logmod.getLogger(__name__)


@dataclass
class InstalCompiledData:
    institutions : list[str] = field(default_factory=list)
    bridges      : list[str] = field(default_factory=list)

class InstalCompiler(metaclass=abc.ABCMeta):
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
    @abc.abstractmethod
    def compile(self, data:ASTs.InstalAST) -> str: pass
