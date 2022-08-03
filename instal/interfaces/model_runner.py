
##-- imports
from __future__ import annotations

import abc
import logging as logmod
import os
from abc import ABCMeta
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from importlib.resources import files
from typing import IO, List

from instal.defaults import COMPILED_EXT
from instal.interfaces.ast import InstalAST, ModelAST
from instal.interfaces.compiler import InstalCompiledData
from instal.util.misc import InstalFileGroup, InstalOptionGroup

##-- end imports




##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class InstalModelRunner(metaclass=ABCMeta):
    """
    InstalModelRunner
    Provdes a top level interface to orchestrate
    parsing -> compilation -> solving -> reporting
    """

    file_group : InstalFileGroup    = field()
    opt_group  : InstalOptionGroup  = field()

    parser     : InstalParser       = field() # Str -> AST
    compiler   : InstalCompiler     = field() # AST -> lp
    solver     : SolverWrapper      = field() # lp -> logic results
    reporter   : InstalReporter     = field() # logic results -> human readable results

    checker    : None|InstalChecker = field(default=None, kw_only=True)

    results    : Any                = field(init=False, default=None)


    def compile_model(self, model_files=None):
        """
        Compile an instal model to a solver readable form
        """
        ir_program    = self.parser.parse(file_group)

        if self.checker is not None:
            self.checker.check(ir_program)

        compiled_data = self.compiler.compile(ir_program)

        # Write the compiled data out
        output_model_files = InstalFileGroup()

        # TODO add prelude as a file

        for inst in compiled_data.institutions:
            # TODO write to file
            # self.output_target + new_file
            # output_model_files.institutions.append(new_file)
            pass

        for bridge in compiled_data.bridges:
            # TODO write to file
            # self.output_target + new_file
            # output_model_files.bridges.append(new_file)
            pass

        return output_model_files

    def get_domain(self, domain_files=None) -> list[Any]:
        """ Get Domain facts for specialize the model with """
        domain_facts = self.parser.get_groundings(domain_files)
        return domain_facts

    def get_facts(self, fact_files=None) -> list[Any]:
        """ Get situation facts to specialize the model with """
        facts = self.parser.get_facts(fact_files)
        return facts


    @abc.abstractmethod
    def solve(self, query_event:list[Any]): pass


    @abc.abstractmethod
    def report(self): pass
