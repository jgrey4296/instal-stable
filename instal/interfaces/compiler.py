##-- imports
from __future__ import annotations

from pathlib import Path
import abc
import pathlib
import logging as logmod
import os
from dataclasses import dataclass, field, InitVar
from instal.util.misc import temporary_text_file
from instal.interfaces.ast import InstalAST, ModelAST, BridgeDefAST, InstitutionDefAST
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

    def compile(self, ir: InstaASTR, pair_outputs=False) -> InstalCompiledData:
        """
        This method strings together compile_ial and compile_bridge - allows subclasses to just deal with them.
        """
        if pair_outputs:
            raise NotImplementedException("Need to do this")

        match ir:
            case ModelAST():
                return self.compile_program(ir)
            case BridgeDefAST():
                return self.compile_bridge
            case InstitutionDefAST():
                return self.compile_institution(ir)
            case TermAST():
                return self.compile_term(ir)
            case TypeAST():
                return self.compile_type(ir)
            case DomainSpecAST():
                return self.compile_domain(ir)
            case EventAST():
                return self.compile_event(ir)
            case FluentAST():
                return self.compile_fluent(ir)
            case ConditionAST():
                return self.compile_condition(ir)
            case RelaitionalAST():
                return self.compile_relaition(ir)
            case ObligationAST():
                return self.compile_obligation(ir)
            case InitiallyAST():
                return self.compile_initially(ir)
            case SinkAST():
                return self.compile_sink(ir)
            case SourceAST():
                return self.compile_source(ir)
            case _:
                raise Exception("Unrecognised top level ir compilation target")

    def compile_program(self, ir: ModelAST) -> InstalCompiledData:
        compiled_data = InstalCompiledData()
        for iir in instal_program.institutions:
            asp : str = self.compile_institution(iir)
            compiled_data.institution.append(asp)

        for bir in instal_program.bridges:
            asp : str = self.compile_bridge(bir, instal_program.institutions)
            compiled_data.bridges.append(asp)

        return compiled_data


    @abc.abstractmethod
    def compile_institution(self, ial: InstitutionDefAST) -> str: pass

    @abc.abstractmethod
    def compile_bridge(self, iab: BridgeDefAST, insts:list[InstitutionDefAST]) -> str: pass
