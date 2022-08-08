##-- imports
from __future__ import annotations

from pathlib import Path
import abc
import pathlib
import logging as logmod
import os
from dataclasses import dataclass, field, InitVar
from instal.util.misc import temporary_text_file
from instal.interfaces import ast as ASTs
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

    def compile_program(self, ir: ASTs.ModelAST) -> InstalCompiledData:
        compiled_data = InstalCompiledData()
        for iir in instal_program.institutions:
            asp : str = self.compile_institution(iir)
            compiled_data.institution.append(asp)

        for bir in instal_program.bridges:
            asp : str = self.compile_bridge(bir, instal_program.institutions)
            compiled_data.bridges.append(asp)

        return compiled_data


    @abc.abstractmethod
    def compile_institution(self, ial: ASTs.InstitutionDefAST) -> str: pass

    @abc.abstractmethod
    def compile_bridge(self, iab: ASTs.BridgeDefAST) -> str: pass


    @abc.abstractmethod
    def compile_domain(self, domain:ASTs.DomainTotalityAST) -> str: pass

    @abc.abstractmethod
    def compile_queries(self, queries:ASTs.QueryTotalityAST) -> str: pass

    @abc.abstractmethod
    def compile_situation(self, facts:ASTs.FactTotalityAST, inst:None|ASTs.InstitutionDefAST) -> str: pass
