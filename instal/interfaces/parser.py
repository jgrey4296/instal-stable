##-- imports
import abc
from typing import IO, List
import instal.util.intermediate_rep as IRs
from instal.util.misc import InstalFileGroup
##-- end imports

class InstalParser(metaclass=abc.ABCMeta):
    """
        InstalParserWrapper
        See __init__.py for more details.
    """

    def parse(self, file_group:InstalFileGroup, save_output_files=None) -> IRs.IR_Program:
        if save_output_files:
            # TODO add this
            raise NotImplementedError(
                "Saving InstAL IR is not available at this time.")

        ir_program : IRs.InstalIR = IRs.IR_Program()
        for path in file_group.institutions:
            ir : IRs.InstalIR = self.parse_ial(i["contents"])
            ir_program.institutions.append(ir)

        for path in file_group.bridges:
            ir : IRs.InstalIR = self.parse_bridge(path, ir_program.institutions)
            ir_program.bridges.append(ir)

        return ir_program

    @abc.abstractmethod
    def parse_institution(self, ial_text) -> IRs.InstalIR: pass

    @abc.abstractmethod
    def parse_bridge(self, bridge_text, ial_ir) -> IRs.InstalIR: pass
