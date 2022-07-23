
##-- imports
from __future__ import annotations

import logging as logmod

from instal.interfaces.compiler import InstalCompiler
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.compiler.bridge_compiler import InstalBridgeCompiler
from instal.util.intermediate_rep import InstalIR, BridgeIR

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalJointCompiler(InstalCompiler):
    """

    """

    def compile_institution(self, ial_ir: dict) -> str:
        """

        input: an ast produced by the instal parser
        output: compiled ASP for that institution
        """
        compiler = InstalInstitutionCompiler()
        return compiler.compile_institution(ial_ir)

    def compile_bridge(self, bridge_ir: InstalIR, ial_ir: InstalIR) -> str:
        """
        input: an ast produced by the instal bridge parser
        output: compiled ASP for that bridge
        """
        source_compiler = InstalInstitutionCompiler()
        sink_compiler   = InstalInstitutionCompiler()
        compiler        = InstalBridgeCompiler(source_compiler, sink_compiler)

        for inst in ial_ir:
            if inst.name == bridge_ir.source
                source_compiler.compile_institution(inst)

            if inst.name == bridge_ir.sink:
                sink_compiler.compile_institution(inst)

        return compiler.compile_bridge(bridge_ast)
