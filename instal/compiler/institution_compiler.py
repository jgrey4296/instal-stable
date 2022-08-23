##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from importlib.resources import files

from instal.errors import InstalCompileError
from instal.interfaces.compiler import InstalCompiler
from instal.interfaces import ast as IAST
from instal.compiler.util import CompileUtil
from instal.compiler.situation_compiler import InstalSituationCompiler

##-- end imports

##-- resources
data_path   = files("instal.__data")
inst_data   = data_path / "institution"
bridge_data = data_path / "bridge"

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

class InstalInstitutionCompiler(InstalCompiler):
    """
    """

    def compile(self, ial: IAST.InstitutionDefAST) -> str:
        assert(isinstance(ial, IAST.InstitutionDefAST))
        assert(not isinstance(ial, IAST.BridgeDefAST))
        self.clear()
        self.insert(INST_PRELUDE,
                    institution=CompileUtil.compile_term(ial.head),
                    source_file=ial.parse_source)
        self.insert(HEADER, header='Part 1: Initial Setup and types', sub="")

        self.compile_events(ial)
        self.compile_fluents(ial)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_generation(ial)
        self.compile_nif_rules(ial)

        self.insert(HEADER, header='Part 3: Initial Situation Specification', sub="")
        situation          = InstalSituationCompiler()
        compiled_situation = situation.compile(IAST.FactTotalityAST(ial.initial), ial, header=False)
        self.insert(compiled_situation)

        self.compile_types(ial.types)
        self.insert("%% End of {institution}", institution=CompileUtil.compile_term(ial.head))

        return "\n".join(self._compiled_text)

    def compile_types(self, type_list:list[IAST.TypeAST]) -> None:
        # Print types. Also adds a constraint that every type must be grounded.
        self.insert(HEADER, header="Type Grounding and declaration", sub="")
        for t in type_list:
            self.insert(TYPE_PAT, x=t.head.value.lower())

        for t in type_list:
            self.insert(TYPE_GROUND, x=t.head.value.lower())

    def compile_events(self, inst):
        # should be sorted already
        for event in inst.events:
            rhs   : str = ", ".join(sorted(CompileUtil.wrap_types(inst.types, event.head)))
            pattern = None
            match event.annotation:
                case IAST.EventEnum.exogenous:
                    pattern = EXO_EV
                case IAST.EventEnum.institutional:
                    pattern = INST_EV
                case IAST.EventEnum.violation:
                    pattern = VIOLATION_EV
                case _:
                    raise TypeError("Unknown Event Type: %s", event)

            assert(pattern is not None)
            self.insert(pattern,
                        event=CompileUtil.compile_term(event.head),
                        inst=CompileUtil.compile_term(inst.head),
                        rhs=rhs)

        self.insert(NULL_EV, inst=CompileUtil.compile_term(inst.head))

    def compile_fluents(self, inst):
        inst_head : str = CompileUtil.compile_term(inst.head)
        for fluent in inst.fluents:
            rhs : str = ", ".join(sorted(CompileUtil.wrap_types(inst.types, fluent.head)))
            match fluent.annotation:
                case IAST.FluentEnum.inertial:
                    self.insert(IN_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.noninertial:
                    self.insert(NONIN_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.obligation:
                    obligation, deadline, violation = fluent.head.params
                    # TODO handle obligation and deadlines being events or fluents
                    # TODO insert event occured / fluent holdsat into rhs
                    self.insert(OB_FLUENT,
                                fluent=CompileUtil.compile_term(fluent.head),
                                obligation=CompileUtil.compile_term(obligation),
                                deadline=CompileUtil.compile_term(deadline),
                                violation=CompileUtil.compile_term(violation),
                                inst=inst_head,
                                rhs=rhs)
                case IAST.FluentEnum.cross if fluent.head.value == "gpow":
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



    def compile_generation(self, inst):
        inst_head = CompileUtil.compile_term(inst.head)
        for relation in inst.relations:
            conditions  = CompileUtil.compile_conditions(inst, relation.conditions)
            type_guards = CompileUtil.wrap_types(inst.types,
                                                 relation.head,
                                                 *relation.body)

            rhs = ", ".join(sorted(conditions | type_guards))
            match relation.annotation:
                case IAST.RelationalEnum.generates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    delay = "+{relation.delay}" if relation.delay> 0 else ""
                    for state in relation.body:
                        self.insert(GEN_PAT,
                                    event=CompileUtil.compile_term(relation.head),
                                    state=CompileUtil.compile_term(state),
                                    inst=inst_head,
                                    delay=delay,
                                    rhs=rhs)
                case IAST.RelationalEnum.initiates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    for state in relation.body:
                        self.insert(INIT_PAT,
                                    event=CompileUtil.compile_term(relation.head),
                                    state=CompileUtil.compile_term(state),
                                    inst=inst_head,
                                    rhs=rhs)
                case IAST.RelationalEnum.terminates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    for state in relation.body:
                        self.insert(TERM_PAT,
                                    event=CompileUtil.compile_term(relation.head),
                                    state=CompileUtil.compile_term(state),
                                    inst=inst_head,
                                    rhs=rhs)
                case IAST.RelationalEnum.xgenerates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    delay = "+{relation.delay}" if relation.delay > 0 else ""
                    self.insert(X_GEN_PAT,
                                event=CompileUtil.compile_term(relation.head),
                                response=CompileUtil.compile_term(relation.body[0]),
                                source=CompileUtil.compile_term(inst.sources [0]),
                                sink=CompileUtil.compile_term(inst.sinks[0]),
                                bridge=inst_head,
                                delay=delay,
                                rhs=rhs)
                case IAST.RelationalEnum.xinitiates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    self.insert(X_INIT_PAT,
                                source=CompileUtil.compile_term(inst.sources[0]),
                                sink=CompileUtil.compile_term(inst.sinks[0]),
                                bridge=inst_head,
                                fluent=CompileUtil.compile_term(relation.head),
                                response=CompileUtil.compile_term(relation.body[0]),
                                rhs=rhs
                                )
                case IAST.RelationalEnum.xterminates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    self.insert(X_TERM_PAT,
                                source=CompileUtil.compile_term(inst.sources[0]),
                                sink=CompileUtil.compile_term(inst.sinks[0]),
                                bridge=inst_head,
                                fluent=CompileUtil.compile_term(relation.head),
                                response=CompileUtil.compile_term(relation.body[0]),
                                rhs=rhs)
                case _:
                    raise TypeError("Unrecognized Relation Type: %s", relation)


    def compile_nif_rules(self, inst):
        for rule in inst.nif_rules:
            conditions = CompileUtil.compile_conditions(inst, rule.body)
            types      = CompileUtil.wrap_types(inst.types,
                                                rule.head)

            rhs = ", ".join(sorted(conditions | types))

            self.insert(NIF_RULE_PAT,
                        state=CompileUtil.compile_term(rule.head),
                        inst=CompileUtil.compile_term(inst.head),
                        rhs=rhs)



