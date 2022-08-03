
##-- imports
from __future__ import annotations

from string import Template
import logging as logmod
from importlib.resources import files

from instal.errors import InstalCompileError
from instal.interfaces.compiler import InstalCompiler
from instal.interfaces import ast as IAST

##-- end imports

##-- resources
data_path = files("instal.__data")
inst_data = files.joinpath("institution")
bridge_data = files.joinpath("bridge")

HEADER         = Template(data_path.joinpath("header_pattern").read_text())
INST_PRELUDE   = Template(inst_path.joinpath("institution_prelude.lp").read_text())
BRIDGE_PRELUDE = Template(bridge_path.joinpath("bridge_prelude.lp").read_text())

TYPE_PAT       = Template(inst_path.joinpath("type_def_guard.lp").read_text())
TYPE_GROUND    = Template(inst_path.joinpath("type_ground_pattern.lp").read_text())

INITIAL_FACT   = Template(inst_path.joinpath("initial_fact_pattern.lp").read_text())
BRIDGE_INITIAL = Template(bridge_path.joinpath("initial_fact_pattern.lp").read_text())

EXO_EV         = Template(inst_path.joinpath("exogenous_event_pattern.lp").read_text())
INST_EV        = Template(inst_path.joinpath("inst_event_pattern.lp").read_text())
VIOLATION_EV   = Template(inst_path.joinpath("violation_event_pattern.lp").read_text())
NULL_EV        = Template(inst_path.joinpath("null_event_pattern.lp").read_text())

IN_FLUENT      = Template(inst_path.joinpath("inertial_fluent_pattern.lp").read_text())
NONIN_FLUENT   = Template(inst_path.joinpath("noninertial_fluent_pattern.lp").read_text())
OB_FLUENT      = Template(inst_path.joinpath("obligation_fluent_pattern.lp").read_text())

CROSS_FLUENT   = Template(bridge_path.joinpath("cross_fluent.lp").read_text())
GPOW_FLUENT    = Template(bridge_path.joinpath("gpow_fluent.lp").read_text())

GEN_PAT        = Template(inst_path.joinpath("generate_rule_pattern.lp").read_text())
INIT_PAT       = Template(inst_path.joinpath("initiate_rule_pattern.lp").read_text())
TERM_PAT       = Template(inst_path.joinpath("terminate_rule_pattern.lp").read_text())

X_GEN_PAT      = Template(bridge_path.joinpath("xgenerate_rule_pattern.lp").read_text())
X_INIT_PAT     = Template(bridge_path.joinpath("xinitiate_rule_pattern.lp").read_text())
X_TERM_PAT     = Template(bridge_path.joinpath("xterminate_rule_pattern.lp").read_text())

NIF_RULE_PAT   = Template(inst_path.joinpath("nif_rule_pattern.lp").read_text())

##-- end resources

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalInstitutionCompiler(InstalCompiler):
    """
    InstalCompiler
    Compiles InstAL IR to ASP.
    Main Access points are compile_(institution/bridge/domain/queries/situation)

    Asssembles a list of strings in self._compiled_text,
    then joins it together after everything is processed.

    self.insert is a utility function to provide substitutions to template patterns
    """

    def __init__(self):
        self._compiled_text : list[str] = []

    def clear(self):
        self._compiled_text = []
    def insert(pattern:str|Template, **kwargs):
        """
        insert a given pattern text into the compiled output,
        formatting it with kwargs.
        """
        match pattern:
            case Template():
                self._compiled_text.append(pattern.safe_substitute(kwargs))
            case str if not bool(kwargs):
                self._compiled_text.append(pattern)
            case str:
                self._compiled_text.append(pattern.format_map(kwargs))
            case _:
                raise TypeError("Unrecognised compile pattern type", pattern)

    def compile_institution(self, ial: IAST.InstitutionDefAST) -> str:
        assert(isinstance(ial, IAST.InstitutionDefAST))
        assert(not isinstance(ial, IAST.BridgeDefAST))
        self.clear()
        self.insert(INST_PRELUDE, institution=ial.head, source_file=ial.source)
        self.insert(HEADER, header='Part 1: Initial Setup and types', sub="")

        self.compile_events(ial)
        self.compile_fluents(ial)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_generation(ial)
        self.compile_nif_rules(ial)

        self.insert(HEADER, header='Part 3: Initial Situation Specification', sub="")
        self.compile_situation(ial.initial, ial)

        self.compile_types(ial.types)
        self.insert("%% End of {institution}", institution=ial.head)

        return "\n".join(self._compiled_text)

    def compile_bridge(self, iab: IAST.BridgeDefAST, insts:list[IAST.InstitutionDefAST]) -> str:
        assert(isinstance(iab, IAST.BridgeDefAST))
        assert(len(iab.sources) == 1)
        assert(len(iab.sinks) == 1)
        self.clear()
        self.insert(BRIDGE_PRELUDE,
                    bridge=iab.head,
                    source=iab.sources[0],
                    sink=iab.sinks[0])

        self.insert(HEADER, header='Part 1: Events and Fluents', sub="")
        self.compile_events(iab)
        self.compile_fluents(iab)

        self.insert(HEADER, header='Part 2: Generation and Consequence', sub="")
        self.compile_generation(iab)
        self.compile_nif_rules(iab)

        self.insert(HEADER, header='Part 3: Initial State', sub="")
        self.compile_situation(iab.initial, iab)

        self.compile_types(iab.types)
        self.insert("%% End of {bridge}", bridge=iab.head)

        return "\n".join(self._compiled_text)

    def compile_domain(self, domain:list[IAST.DomainSpecAST]) -> str:
        """
        Compile idc domain specs of Type: instance, instance, instance...
        """
        assert(all(isinstance(x, IAST.DomainSpecAST) for x in domain))
        self.clear()
        self.insert(HEADER, header="Domain Specification", sub=domain.source)
        for assignment in domain:
            wrapper = assignment.head.head.lower()
            for term in assignment.terms:
                assert(not bool(term.params))
                self.insert(f"{wrapper}({term}).")

        return "\n".join(self._compiled_text)

    def compile_queries(self, query:list[IAST.TermAST]) -> str:
        """
        Compile sequence of observations into extObserved facts
        # TODO handle specifying time of observation
        """
        assert(all(isinstance(x, IAST.TermAST) for x in query))
        self.clear()
        self.insert(HEADER, header="Query Specification", sub=query.source)
        for i, term in enumerate(query):
            params = ", ".join(term.params)
            self.insert(f"extObserved({params}, {i}).")
            self.insert(f"_eventSet({i}).")

        return "\n".join(self._compiled_text)

    def compile_types(self, type_list:list[IAST.TypeAST]) -> None:
        # Print types. Also adds a constraint that every type must be grounded.
        self.insert(HEADER, header="Type Grounding and declaration", sub="")
        for t in type_list:
            self.insert(TYPE_PAT, x=t.head.head.lower())

        for t in type_list:
            self.insert(TYPE_GROUND, x=t.head.head.lower())

    def compile_events(self, inst):
        # should be sorted already
        for event in inst.events:
            rhs   : str = CompileUtil.wrap_types(inst.types, event.head)
            event : str = str(event)
            pattern = None
            match event.annotation:
                case IAST.EventEnum.exogenous:
                    pattern = EXO_EV
                case IAST.EventEnum.institution:
                    pattern = INST_EV
                case IAST.EventEnum.violation:
                    pattern = VIOLATION_EV
                case _:
                    raise TypeError("Unknown Event Type: %s", event)

            assert(pattern is not None)
            self.insert(pattern,
                        event=str(event),
                        inst=inst.head,
                        rhs=rhs)

        self.insert(NULL_EVENT, inst=inst.head)

    def compile_fluents(self, inst):
        for fluent in inst.fluents:
            rhs : str = CompileUtil.wrap_types(inst.types, fluent.head)
            match fluent.annotation:
                case IAST.FluentEnum.noninertial:
                    self.insert(NONIN_FLUENT,
                                fluent=str(fluent.head),
                                inst=inst.head,
                                rhs=rhs)
                case IAST.FluentEnum.obligation:
                    obligation, deadline, violation = fluent.head.params
                    # TODO handle obligation and deadlines being events or fluents
                    # TODO insert event occured / fluent holdsat into rhs
                    self.insert(OB_FLUENT,
                                fluent=str(fluent)
                                obligation=obligation,
                                deadline=deadline,
                                violation=violation,
                                inst=inst.head,
                                rhs=rhs)
                case IAST.FluentEnum.cross if fluent.head.head == gpow:
                    assert(len(fluent.head.params) == 3)
                    self.insert(GPOW_FLUENT,
                                source=fluent.head.params[0],
                                event=fluent.head.params[1],
                                sink=fluent.head.params[2],
                                bridge=inst.head,
                                rhs=rhs)
                case IAST.FluentEnum.cross:
                    assert(len(fluent.head.params) == 3)
                    self.insert(CROSS_FLUENT,
                                power=fluent.head.head,
                                source=fluent.head.params[0],
                                fluent=fluent.head.params[1],
                                sink=fluent.head.params[2],
                                bridge=inst.head,
                                rhs=rhs)
                case _:
                    self.insert(IN_FLUENT,
                                fluent=str(fluent.head),
                                inst=inst.head,
                                rhs=rhs)



    def compile_generation(self, inst):
        for relation in inst.relations:
            conditions  = CompileUtil.compile_conditions(inst, relation.conditions)
            type_guards = CompileUtil.wrap_types(inst.types,
                                                 relation.head,
                                                 *relation.body)

            rhs = f"{conditions}, {type_guards}"

            match relation.annotation:
                case IAST.RelationalEnum.generates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    delay = "+{relation.time}" if relation.time > 0 else ""
                    self.insert(GEN_PAT,
                                event=str(relation.head),
                                state=relation.body,
                                inst=inst.head,
                                delay=delay,
                                rhs=rhs)
                case IAST.RelationalEnum.initiates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self.insert(GEN_PAT,
                                event=str(relation.head),
                                state=relation.body,
                                inst=inst.head,
                                rhs=rhs)
                case IAST.RelationalEnum.terminates:
                    assert(not isinstance(inst, IAST.BridgeDefAST))
                    self.insert(GEN_PAT,
                                event=str(relation.head),
                                state=relation.body,
                                inst=inst.head,
                                rhs=rhs)
                case IAST.RelationalEnum.xgenerates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    delay = "+{relation.time}" if relation.time > 0 else ""
                    self.insert(X_GEN_PAT,
                                event=relation.head,
                                response=event.body[0],
                                source=inst.source[0],
                                sink=inst.sink[0],
                                bridge=inst.head,
                                delay=delay
                                rhs=rhs)
                case IAST.RelationalEnum.xinitiates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    self.insert(X_INIT_PAT,
                                source=inst.sources[0],
                                sink=inst.sinks[0],
                                bridge=inst.head,
                                fluent=relation.head,
                                response=relation.body[0],
                                rhs=rhs
                                )
                case IAST.RelationalEnum.xterminates:
                    assert(isinstance(inst, IAST.BridgeDefAST))
                    self.insert(X_TERM_PAT,
                                source=inst.source[0],
                                sink=inst.sinks[0],
                                bridge=inst.head,
                                fluent=relation.head,
                                response=relation.body[0],
                                rhs=rhs)
                case _:
                    raise TypeError("Unrecognized Relation Type: %s", relation)


    def compile_nif_rules(self, inst):
        for rule in inst.nif_rules:
            rhs = CompileUtil.wrap_types(inst.types,
                                         rule.head,
                                         *rule.body)
            self.insert(NIF_RULE_PAT,
                        state=str(rule.head),
                        inst=inst.head,
                        rhs=rhs)



    def compile_situation(self, facts:list[IAST.InitiallyAST], inst:None|IAST.InstitutionDefAST=None):
        assert(all(isinstance(x, IAST.InitiallyAST) for x in facts))
        for initial in facts:
            for state in initial.body:
                if inst:
                    conditions  = CompileUtil.compile_conditions(inst, initial.conditions)
                    type_guards = CompileUtil.wrap_types(inst.types, state.head)
                    rhs = f"{conditions}, {type_guards}"
                    self.insert(INITIAL_FACT,
                                state=str(state),
                                inst=inst.head,
                                rhs=rhs)
                else:
                    assert(initial.inst is not None)
                    assert(not bool(initial.conditions))
                    rhs = CompileUtil.wrap_types(None, state.head)
                    self.insert(INITIAL_FACT,
                                state=str(state),
                                inst=initial.inst,
                                rhs=rhs)






class CompileUtil:
    @staticmethod
    def wrap_types(types:list[IAST.TypeAST], *params:IAST.TermAST) -> str:
        """
        convert instal variables (User, Book etc)
        to terms for the right hand side of rules to ensure correct typing:
        user(User), book(Book) etc.
        """
        type_check : set[str] = {x.head for x in types} if bool(types) else set()
        result                = []
        queue                 = list(params)
        found                 = set()
        while bool(queue):
            param = queue.pop()
            if param in found:
                continue
            if not param.is_var:
                queue += param.params
                continue
            assert(not bool(param.params))
            assert(param.head[0].isupper())
            assert(not bool(type_check) or param.head in type_check)
            # TODO handle variable numbers
            result.append(f"{param.head.lower()}({param.head})")
            found.add(param)

        if bool(result):
            return ", ".join(result)
        else:
            return "true"


    @staticmethod
    def compile_conditions(inst, all_conditions) -> str:
        if not bool(conds):
            return "true"

        results = []
        for condition in all_conditions:
            cond : list[str] = []
            if condition.negated:
                cond.append("not ")

            if condition.operator is None and condition.rhs is None:
                term = CompileUtil.compile_term(condition.head)
                results.append(CompileUtil.wrap_types(inst.types, condition.head))
                cond.append(f"holdsat({term}, {inst.head}, I)")
            else:
                assert(condition.operator is not None and condition.rhs is not None)
                results.append(CompileUtil.wrap_types(inst.types, condition.head, condition.rhs))
                cond.append(CompileUtil.compile_term(condition.head))
                cond.append(condtion.operator)
                cond.append(CompileUtil.compile_term(condition.rhs))

            results.append("".join(cond))


        return ", ".join(results)


    @staticmethod
    def compile_term(term) -> str:
        params = [CompileUtil.compile_term(x) for x in term.params]
        return f"{term.head}({', '.join(params)})"

