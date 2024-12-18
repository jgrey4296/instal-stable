##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from importlib.resources import files

from instal.errors import InstalCompileError
from instal.interfaces.compiler import InstalCompiler_i
from instal.interfaces import ast as IAST
from instal.compiler.util import CompileUtil
from instal.compiler.situation_compiler import InstalSituationCompiler
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.defaults import COMP_DATA_loc, STANDARD_PRELUDE_loc

##-- end imports

##-- resources
data_path   = files(COMP_DATA_loc)
try:
    inst_prelude = files(STANDARD_PRELUDE_loc)
except ModuleNotFoundError:
    inst_prelude = data_path / STANDARD_PRELUDE_loc

HEADER             = Template((data_path / "header_pattern").read_text())
INST_PRELUDE       = Template((data_path / "institution_prelude.lp").read_text())
BRIDGE_PRELUDE     = Template((data_path / "bridge_prelude.lp").read_text())

TYPE_PAT           = Template((data_path / "type_def_guard.lp").read_text())
TYPE_GROUND        = Template((data_path / "type_ground_pattern.lp").read_text())

INITIAL_FACT       = Template((data_path / "initial_fact_pattern.lp").read_text())

EVENT_PATTERN      = Template((data_path / "event_pattern.lp").read_text())

INERTIAL_FLUENT    = Template((data_path / "inertial_fluent_pattern.lp").read_text())
TRANSIENT_FLUENT   = Template((data_path / "transient_fluent_pattern.lp").read_text())
OB_FLUENT          = Template((data_path / "obligation_fluent_pattern.lp").read_text())

GEN_PAT            = Template((data_path / "generate_rule_pattern.lp").read_text())
INIT_PAT           = Template((data_path / "initiate_rule_pattern.lp").read_text())
TERM_PAT           = Template((data_path / "terminate_rule_pattern.lp").read_text())

TRANSIENT_RULE_PAT = Template((data_path / "transient_rule_pattern.lp").read_text())

##-- end resources

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalInstitutionCompiler(InstalCompiler_i):
    """
    """

    def load_prelude(self) -> str:
        text = []
        if inst_prelude.is_dir():
            for path in sorted(x for x in inst_prelude.iterdir() if x.suffix == ".lp"):
                text += path.read_text().split("\n")
        else:
            assert(inst_prelude.is_file())
            text.append(inst_prelude.read_text())

        text.append("%% End of Prelude")

        return "\n".join(text)

    def compile(self, ials: list[IAST.InstitutionDefAST]) -> str:
        logging.debug("Compiling %s Institutions", len(ials))
        self.clear()
        for ial in ials:
            self.compile_inst(ial)

        return self.compilation

    def compile_inst(self, ial: IAST.InstitutionDefAST):
        logging.debug("Compiling Institution")
        assert(isinstance(ial, IAST.InstitutionDefAST))
        assert(not isinstance(ial, IAST.BridgeDefAST))
        self.insert(INST_PRELUDE,
                    institution=CompileUtil.compile_term(ial.head),
                    source_file=ial.sources_str)
        self.insert(HEADER, header='Part 1: Initial Setup and types', sub="")

        self.compile_events(ial)
        self.compile_fluents(ial)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_rules(ial)

        self.insert(HEADER, header='Part 3: Initial Situation Specification', sub="")
        situation          = InstalSituationCompiler()
        compiled_situation = situation.compile(ial.initial, ial, header=False)
        self.insert(compiled_situation)

        self.compile_types(ial.types)
        self.insert("%% End of {institution}", institution=CompileUtil.compile_term(ial.head))


    def compile_types(self, type_list:list[IAST.DomainSpecAST]) -> None:
        logging.debug("Compiling Types")
        # Print types. Also adds a constraint that every type must be grounded.
        self.insert(HEADER, header="Type Grounding and declaration", sub="")
        domain_compiler = InstalDomainCompiler()

        with_values = [x for x in type_list if bool(x.body)]
        if bool(with_values):
            self.insert(domain_compiler.compile(with_values))

        for t in type_list:
            self.insert(TYPE_PAT, x=t.head.value.lower())

        for t in type_list:
            self.insert(TYPE_GROUND, x=t.head.value.lower())

    def compile_events(self, inst):
        logging.debug("Compiling Events")
        # should be sorted already
        for event in inst.events:
            rhs   : str = ", ".join(sorted(CompileUtil.wrap_types(inst.types, event.head)))
            etype   = None
            match event.annotation:
                case IAST.EventEnum.exogenous:
                    etype = "ex"
                case IAST.EventEnum.institutional:
                    etype = "inst"
                case IAST.EventEnum.violation:
                    etype = "viol"
                case _:
                    raise TypeError("Unknown Event Type: %s", event)

            assert(etype is not None)
            self.insert(EVENT_PATTERN,
                        event=CompileUtil.compile_term(event.head),
                        inst=CompileUtil.compile_term(inst.head),
                        etype=etype,
                        etype_full=event.annotation,
                        rhs=rhs)

    def compile_fluents(self, inst, *, fluents=None):
        logging.debug("Compiling Fluents")
        inst_head : str = CompileUtil.compile_term(inst.head)
        for fluent in fluents or inst.fluents:
            rhs : str = ", ".join(sorted(CompileUtil.wrap_types(inst.types, fluent.head)))

            match fluent.annotation:
                case IAST.FluentEnum.inertial:
                    self.insert(INERTIAL_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.transient:
                    self.insert(TRANSIENT_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.obligation | IAST.FluentEnum.achievement_obligation | IAST.FluentEnum.maintenance_obligation:
                    obl_name = fluent.head.value
                    obl_type = "achievement"
                    requirement, deadline, violation = fluent.head.params

                    if fluent.annotation is IAST.FluentEnum.maintenance_obligation:
                        obl_type = "maintenance"

                    self.insert(OB_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                name=obl_name,
                                requirement=CompileUtil.compile_term(requirement),
                                deadline=CompileUtil.compile_term(deadline),
                                violation=CompileUtil.compile_term(violation),
                                obType=obl_type,
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.cross if fluent.head.value == "genPow":
                    assert(len(fluent.head.params) == 3)
                    self.insert(GPOW_FLUENT,
                                source=CompileUtil.compile_term(fluent.head.params[0]),
                                event=CompileUtil.compile_term(fluent.head.params[1]),
                                sink=CompileUtil.compile_term(fluent.head.params[2]),
                                bridge=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.cross:
                    assert(len(fluent.head.params) == 3)
                    self.insert(CROSS_FLUENT,
                                power=fluent.head.value,
                                source=CompileUtil.compile_term(fluent.head.params[0]),
                                fluent=CompileUtil.compile_term(fluent.head.params[1]),
                                sink=CompileUtil.compile_term(fluent.head.params[2]),
                                bridge=inst_head,
                                rhs=rhs)
                case _:
                    raise TypeError("Unrecognized fluent type: ", fluent.annotation)



    def compile_rules(self, inst, *, rules=None):
        logging.debug("Compiling Institution Rules")
        inst_head = CompileUtil.compile_term(inst.head)

        for rule in rules or inst.rules:
            assert(isinstance(rule, IAST.RuleAST))
            conditions  = CompileUtil.compile_conditions(inst, rule.conditions)
            type_guards = CompileUtil.wrap_types(inst.types,
                                                 rule.head,
                                                 *rule.body)

            rhs = ", ".join(sorted(conditions | type_guards))
            match rule.annotation:
                case IAST.RuleEnum.generates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self._compile_generation(rule, rhs, inst_head)
                case IAST.RuleEnum.initiates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self._compile_initiation(rule, rhs, inst_head)
                case IAST.RuleEnum.terminates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self._compile_termination(rule, rhs, inst_head)
                case IAST.RuleEnum.transient:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self._compile_transient(rule, rhs, inst_head)
                case _:
                    raise TypeError("Unrecognized Relation Type: %s", rule)


    def _compile_generation(self, rule, rhs, inst_head):
        delay = "+{rule.delay}" if rule.delay > 0 else ""
        for event in rule.body:
            self.insert(GEN_PAT,
                        source_event=CompileUtil.compile_term(rule.head),
                        result_event=CompileUtil.compile_term(event),
                        inst=inst_head,
                        delay=delay,
                        rhs=rhs)

    def _compile_initiation(self, rule, rhs, inst_head):
        for state in rule.body:
            self.insert(INIT_PAT,
                        event=CompileUtil.compile_term(rule.head),
                        state=CompileUtil.compile_term(state),
                        inst=inst_head,
                        rhs=rhs)

    def _compile_termination(self, rule, rhs, inst_head):
        for state in rule.body:
            self.insert(TERM_PAT,
                        event=CompileUtil.compile_term(rule.head),
                        state=CompileUtil.compile_term(state),
                        inst=inst_head,
                        rhs=rhs)

    def _compile_transient(self, rule, rhs, inst_head):
        self.insert(TRANSIENT_RULE_PAT,
                    state=CompileUtil.compile_term(rule.body[0]),
                    inst=inst_head,
                    rhs=rhs)
