
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
from instal.defaults import INSTITUTION_DATA_loc, BRIDGE_DATA_loc, DATA_loc

##-- end imports

##-- resources
data_path   = files(DATA_loc)
inst_data   = files(INSTITUTION_DATA_loc)
bridge_data = files(BRIDGE_DATA_loc)

HEADER         = Template((data_path   / "header_pattern").read_text())
INST_PRELUDE   = Template((inst_data   / "institution_prelude.lp").read_text())
BRIDGE_PRELUDE = Template((bridge_data / "bridge_prelude.lp").read_text())

TYPE_PAT       = Template((inst_data   / "type_def_guard.lp").read_text())
TYPE_GROUND    = Template((inst_data   / "type_ground_pattern.lp").read_text())

INITIAL_FACT   = Template((inst_data   / "initial_fact_pattern.lp").read_text())

EXO_EV         = Template((inst_data   / "exogenous_event_pattern.lp").read_text())
INST_EV        = Template((inst_data   / "inst_event_pattern.lp").read_text())
VIOLATION_EV   = Template((inst_data   / "violation_event_pattern.lp").read_text())
NULL_EV        = Template((inst_data   / "null_event_pattern.lp").read_text())

IN_FLUENT      = Template((inst_data   / "inertial_fluent_pattern.lp").read_text())
NONIN_FLUENT   = Template((inst_data   / "noninertial_fluent_pattern.lp").read_text())
OB_FLUENT      = Template((inst_data   / "obligation_fluent_pattern.lp").read_text())

CROSS_FLUENT   = Template((bridge_data / "cross_fluent.lp").read_text())
GPOW_FLUENT    = Template((bridge_data / "gpow_cross_fluent.lp").read_text())

GEN_PAT        = Template((inst_data   / "generate_rule_pattern.lp").read_text())
INIT_PAT       = Template((inst_data   / "initiate_rule_pattern.lp").read_text())
TERM_PAT       = Template((inst_data   / "terminate_rule_pattern.lp").read_text())

X_GEN_PAT      = Template((bridge_data / "xgenerate_rule_pattern.lp").read_text())
X_INIT_PAT     = Template((bridge_data / "xinitiate_rule_pattern.lp").read_text())
X_TERM_PAT     = Template((bridge_data / "xterminate_rule_pattern.lp").read_text())

NIF_RULE_PAT   = Template((inst_data   / "nif_rule_pattern.lp").read_text())

##-- end resources

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalBridgeCompiler(InstalInstitutionCompiler, InstalCompiler_i):
    """
    """

    def compile(self, iab: IAST.BridgeDefAST) -> str:
        assert(isinstance(iab, IAST.BridgeDefAST))
        assert(len(iab.sources) == 1)
        assert(len(iab.sinks) == 1)
        self.clear()
        self.insert(BRIDGE_PRELUDE,
                    bridge=CompileUtil.compile_term(iab.head),
                    source=CompileUtil.compile_term(iab.sources[0]),
                    sink=CompileUtil.compile_term(iab.sinks[0]),
                    source_file=iab.parse_source)

        self.insert(HEADER, header='Part 1: Events and Fluents', sub="")
        self.compile_events(iab)
        self.compile_fluents(iab)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_generation(iab)
        self.compile_nif_rules(iab)

        self.insert(HEADER, header='Part 3: Initial Situation Specification', sub="")
        situation          = InstalSituationCompiler()
        compiled_situation = situation.compile(IAST.FactTotalityAST(iab.initial), iab, header=False)
        self.insert(compiled_situation)

        self.compile_types(iab.types)
        self.insert("%% End of {bridge}", bridge=CompileUtil.compile_term(iab.head))

        return "\n".join(self._compiled_text)

