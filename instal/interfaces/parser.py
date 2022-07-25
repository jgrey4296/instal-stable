##-- imports
import abc
from typing import IO, List
import instal.interfaces.ast as InASTs
from instal.util.misc import InstalFileGroup
##-- end imports

class InstalParser(metaclass=abc.ABCMeta):
    """
        InstalParserWrapper
        See __init__.py for more details.
    """

    def parse(self, file_group:InstalFileGroup) -> InASTs.ProgramAST:
        try:
            text : str = ""
            ir_program : InASTs.InstalAST = InASTs.ProgramAST()
            for path in file_group.institutions:
                with open(path, 'r') as f:
                    text = f.read()
                ir : InASTs.InstalAST = self.parse_institution(text)
                ir_program.institutions.append(ir)

            for path in file_group.bridges:
                with open(path, 'r') as f:
                    text = f.read()
                ir : InASTs.InstalAST = self.parse_bridge(text, ir_program.institutions)
                ir_program.bridges.append(ir)

        except FileNotFoundError as err:
            logging.exception("File Not Found for Parsing: %s", path)

        return ir_program

    @abc.abstractmethod
    def parse_institution(self, text:str) -> InASTs.InstalAST: pass
    @abc.abstractmethod
    def parse_bridge(self, text:str) -> InASTs.InstalAST: pass

    @abc.abstractmethod
    def parse_facts(self, text:str) -> list[InASTs.InstalAST]: pass
    @abc.abstractmethod
    def parse_atoms(self, text:str) -> list[InASTs.InstalAST]: pass
