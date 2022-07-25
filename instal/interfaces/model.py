
##-- imports
from __future__ import annotations

import logging as logmod
import os
from abc import ABCMeta
from collections import defaultdict
from importlib.resources import files
from typing import IO, List

from instal import InstalFile
from instal.compiler.InstalCompilerNew import InstalCompilerNew
from instal.defaults import COMPILED_EXT
from instal.domainparser.DomainParser import DomainParser
from instal.factparser.FactParser import FactParser
from instal.instalutility import temporary_text_file
from instal.parser.InstalParserNew import InstalParserNew
from instal.state.InstalStateTrace import InstalStateTrace
from instal.interfaces.compiled_rep import InstalCompiledData
from instal.interfaces.ast import InstalAST, ProgramAST
from instal.util.misc import InstalFileGroup, InstalOptionGroup
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class InstalModel(metaclass=ABCMeta):
    """
        InstalModel
        Wrapper for different implementations of InstAL solving.
        See: InstalMultiShotModel and InstalSingleShotModel
    """

    def __init__(self, file_group:InstalFileGroup, opt_group:InstalOptionGroup,
                 parser:InstalParser, compiler:InstalCompiler,
                 domain_parser, fact_parser):
        self.output_target = opt_group.output

        self.parser        = parser()
        self.compiler      = compiler()
        self.domain_parser = DomainParser()
        self.fact_parser   = FactParser()

        self.model_files   = self.process_model(file_group)
        self.domain_facts  = self.process_domains(file_group)
        self.initial_facts = self.process_facts(file_group)

        self.answersets : list[InstalStateTrace] = []


    def process_model(self, file_group:InstalFileGroup) -> InstalFileGroup:
        ir_program    = self.parser.parse(file_group)
        compiled_data = self.compiler.compile(ir_program)

        # Write the compiled data out
        output_model_files = InstalFileGroup()

        # TODO add prelude as a file

        for inst in compiled_data.institutions:
            # TODO write to file
            # self.output_target + new_file
            # output_model_files.institutions.append(new_file)
            pass

        for bridge in compiled_data["bridge_asp"]:
            # TODO write to file
            # self.output_target + new_file
            # output_model_files.bridges.append(new_file)
            pass

        return output_model_files

    def process_domains(self, file_group:InstalFileGroup) -> defaultdict(set):
        domain_facts = self.domain_parser.get_groundings(domain_files)
        return domain_facts

    def process_facts(self, file_group:InstalFileGroup) -> list[Any]:
        facts = self.fact_parser.get_facts(fact_files)
        return facts


    @abc.abstractmethod
    def solve(self, query_event:list[Any]): pass
