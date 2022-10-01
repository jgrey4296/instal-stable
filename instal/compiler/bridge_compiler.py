
##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from importlib.resources import files

from instal.errors import InstalCompileError
from instal.interfaces.compiler import InstalCompiler_i
from instal.interfaces import ast as IAST
from instal.compiler.util import CompileUtil
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.compiler.situation_compiler import InstalSituationCompiler
from instal.defaults import COMP_DATA_loc

##-- end imports

##-- resources
data_path      = files(DATA_loc)

HEADER         = Template((data_path / "header_pattern").read_text())
BRIDGE_PRELUDE = Template((data_path / "bridge_prelude.lp").read_text())

##-- end resources

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalBridgeCompiler(InstalInstitutionCompiler, InstalCompiler_i):
    """
    """

    def compile(self, iabs: list[IAST.BridgeDefAST]) -> str:
        logging.debug("Compiling %s Bridges", len(ials))
        self.clear()
        for iab in iabs:
            self.compile_bridge(iab)

        return self.compilation

    def compile_bridge(self, iab):
        assert(isinstance(iab, IAST.BridgeDefAST))
        assert(len(iab.sources) == 1)
        assert(len(iab.sinks) == 1)
        self.insert(BRIDGE_PRELUDE,
                    bridge=CompileUtil.compile_term(iab.head),
                    source=CompileUtil.compile_term(iab.sources[0]),
                    sink=CompileUtil.compile_term(iab.sinks[0]),
                    source_file=iab.sources_str)

        self.insert(HEADER, header='Part 1: Events and Fluents', sub="")
        self.compile_events(iab)
        self.compile_fluents(iab)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_rules(iab)

        self.insert(HEADER, header='Part 3: Initial Situation Specification', sub="")
        situation          = InstalSituationCompiler()
        compiled_situation = situation.compile(iab.initial, iab, header=False)
        self.insert(compiled_situation)

        self.compile_types(iab.types)
        self.insert("%% End of {bridge}", bridge=CompileUtil.compile_term(iab.head))
