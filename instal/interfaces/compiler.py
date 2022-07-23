##-- imports
from __future__ import annotations

from pathlib import Path
import abc
import pathlib
import logging as logmod
import os
from dataclasses import dataclass, field, InitVar
from instal.util.misc import temporary_text_file
from instal.util.compiled_rep import InstalCompiledData
from isntal.util.intermediate_rep import InstalIR, IR_Program, BridgeIR, InstitutionIR
##-- end imports

logging = logmod.getLogger(__name__)


class InstalCompiler(metaclass=abc.ABCMeta):
    """
    Interface for compiling InstalIR down to a
    specific solver format
    """

    def compile(self, ir: InstalIR, pair_outputs=False) -> InstalCompiledData:
        """
        This method strings together compile_ial and compile_bridge - allows subclasses to just deal with them.
        """
        if pair_outputs:
            raise NotImplementedException("Need to do this")

        match ir:
            case IR_Program():
                return self.compile_program(ir)
            case BridgeIR():
                return self.compile_bridge
            case InstitutionIR():
                return self.compile_institution(ir)
            case _:
                raise Exception("Unrecognised top level ir compilation target")

    def compile_program(self, ir: IR_Program) -> InstalCompiledData:
        compiled_data = InstalCompiledData()
        for iir in instal_program.institutions:
            asp : str = self.compile_ial(iir)
            compiled_data.institution.append(asp)

        for bir in instal_program.bridges:
            asp : str = self.compile_bridge(bir, instal_program.institutions)
            compiled_data.bridges.append(asp)

        return compiled_data

    @abc.abstractmethod
    def compile_institution(self, inst_ir: InstitutionIR) -> str:
        """

        input: an ast produced by the instal parser
        output: compiled ASP for that institution
        """
        pass

    @abc.abstractmethod
    def compile_bridge(self, bridge_ir: BridgeIR, inst_ir: InstitutionIR) -> str:
        """
        input: an ast produced by the instal bridge parser
        output: compiled ASP for that bridge
        """
        pass
