
##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from importlib.resources import files

from instal.errors import InstalCompileError
from dataclasses import dataclass, field, InitVar
from instal.interfaces.compiler import InstalCompiler_i
from instal.interfaces import ast as IAST
from instal.compiler.util import CompileUtil
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.compiler.situation_compiler import InstalSituationCompiler
from instal.defaults import COMP_DATA_loc

##-- end imports

##-- resources
data_path      = files(COMP_DATA_loc)

HEADER         = Template((data_path / "header_pattern").read_text())
BRIDGE_PRELUDE = Template((data_path / "bridge_prelude.lp").read_text())
LINK_PATTERN   = Template((data_path / "link_pattern.lp").read_text())
CROSS_FLUENT   = Template((data_path / "cross_fluent.lp").read_text())
GPOW_FLUENT    = Template((data_path / "gpow_cross_fluent.lp").read_text())
X_GEN_PAT      = Template((data_path / "xgenerate_rule_pattern.lp").read_text())
X_INIT_PAT     = Template((data_path / "xinitiate_rule_pattern.lp").read_text())
X_TERM_PAT     = Template((data_path / "xterminate_rule_pattern.lp").read_text())

##-- end resources

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@dataclass
class InstalBridgeCompiler(InstalInstitutionCompiler, InstalCompiler_i):
    """
    """

    sources : set[str] = field(init=False, default_factory=set)
    sinks   : set[str] = field(init=False, default_factory=set)

    def compile(self, iabs: list[IAST.BridgeDefAST]) -> str:
        logging.debug("Compiling %s Bridges", len(iabs))
        self.clear()
        for iab in iabs:
            self.compile_bridge(iab)

        return self.compilation

    def compile_bridge(self, iab):
        assert(isinstance(iab, IAST.BridgeDefAST))

        self.insert(BRIDGE_PRELUDE,
                    bridge=CompileUtil.compile_term(iab.head),
                    source_file=iab.sources_str)

        self.compile_links(iab)

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

    def compile_links(self, iab, as_data=False):
        bridge_name = CompileUtil.compile_term(iab.head)
        for link in iab.links:
            term = CompileUtil.compile_term(link.head)
            match link.link_type:
                case IAST.BridgeLinkEnum.sink:
                    self.sinks.add(term)
                case IAST.BridgeLinkEnum.source:
                    self.sources.add(term)

            if not as_data:
                self.insert(LINK_PATTERN,
                            link_type=link.link_type.name,
                            name=term,
                            bridge=bridge_name)




    def compile_rules(self, iab, *, rules=None):
        logging.debug("Compiling Bridge Rules")
        assert(isinstance(iab, IAST.BridgeDefAST))
        iab_head = CompileUtil.compile_term(iab.head)
        base_inst_rules = []

        if (not bool(self.sources)) or (not bool(self.sinks)):
            self.compile_links(iab, as_data=True)

        source = list(self.sources)[0]
        sink  =  list(self.sinks)[0]

        for rule in rules or iab.rules:
            assert(isinstance(rule, IAST.RuleAST))
            conditions  = CompileUtil.compile_conditions(iab, rule.conditions)
            type_guards = CompileUtil.wrap_types(iab.types,
                                                 rule.head,
                                                 *rule.body)

            rhs = ", ".join(sorted(conditions | type_guards))

            match rule.annotation:
                case IAST.RuleEnum.xgenerates:
                    delay = "+{rule.delay}" if rule.delay > 0 else ""
                    self.insert(X_GEN_PAT,
                                event=CompileUtil.compile_term(rule.head),
                                response=CompileUtil.compile_term(rule.body[0]),
                                source=source,
                                sink=sink,
                                bridge=iab_head,
                                delay=delay,
                                rhs=rhs)
                case IAST.RuleEnum.xinitiates:
                    self.insert(X_INIT_PAT,
                                source=source,
                                sink=sink,
                                bridge=iab_head,
                                fluent=CompileUtil.compile_term(rule.head),
                                response=CompileUtil.compile_term(rule.body[0]),
                                rhs=rhs
                                )
                case IAST.RuleEnum.xterminates:
                    self.insert(X_TERM_PAT,
                                source=source,
                                sink=sink,
                                bridge=iab_head,
                                fluent=CompileUtil.compile_term(rule.head),
                                response=CompileUtil.compile_term(rule.body[0]),
                                rhs=rhs)
                case _:
                    base_iab_rules.append(rule)

        if bool(base_inst_rules):
            super().compile_rules(iab, rules=base_inst_rules)


    def compile_fluents(self, iab, *, fluents=None):
        logging.debug("Compiling Bridge Fluents")
        iab_head : str   = CompileUtil.compile_term(iab.head)
        base_inst_fluents = []

        if (not bool(self.sources)) or (not bool(self.sinks)):
            self.compile_links(iab, as_data=True)

        source = list(self.sources)[0]
        sink  =  list(self.sinks)[0]

        for fluent in fluents or iab.fluents:
            rhs : str = ", ".join(sorted(CompileUtil.wrap_types(iab.types, fluent.head)))

            match fluent.annotation:
                case IAST.FluentEnum.cross if fluent.head.value == "gpow":
                    assert(len(fluent.head.params) == 3)
                    self.insert(GPOW_FLUENT,
                                event=CompileUtil.compile_term(fluent.head.params[1]),
                                source=source,
                                sink=sink,
                                bridge=iab_head,
                                rhs=rhs)
                case IAST.FluentEnum.cross:
                    assert(len(fluent.head.params) == 3)
                    self.insert(CROSS_FLUENT,
                                power=fluent.head.value,
                                fluent=CompileUtil.compile_term(fluent.head.params[1]),
                                source=source,
                                sink=sink,
                                bridge=iab_head,
                                rhs=rhs)
                case _:
                    base_inst_fluents.append(fluent)

        if bool(base_inst_fluents):
            super().compile_fluents(iab, fluents=base_inst_fluents)
