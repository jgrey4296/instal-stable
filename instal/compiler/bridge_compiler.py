
##-- imports
from __future__ import annotations

import logging as logmod
from importlib.resources import files

from instal.interfaces.compiler import InstalCompiler
##-- end imports

##-- data
data_path      = files("instal.__data")
bridge_prelude = data_path.joinpath("bridge_prelude.pattern.lp").read_text()
##-- end data

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalBridgeCompiler(InstalCompiler):
    """
        InstalBridgeCompiler
        Compiles InstAL Bridge IR to ASP.
        Call compile_bridge() - requires the IR and an InstalCompiler instance corresponding to source + sink.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self, source_compiler: InstalCompiler, sink_compiler: InstalCompiler):
        super().__init__()
        self.bridge_ir       = {}
        self.source_compiler = source_compiler
        self.sink_compiler   = sink_compiler
        self.types           = {}
        self.out             = ""

    def compile_bridge(self, bridge_ir: dict) -> str:
        """Called to compile bridge_ir to ASP."""
        self.bridge_ir = bridge_ir

        for k, v in self.source_compiler.types.items():
            self.types[k] = v
        for k, v in self.sink_compiler.types.items():
            self.types[k] = v

        self.names = bridge_ir["names"]

        self.bridge_print_standard_prelude()
        self.bridge_print_constraints()
        self.bridge_print_cross_initiation_fluents(bridge_ir["cross_initiation_fluents"])
        self.bridge_print_cross_termination_fluents(bridge_ir["cross_termination_fluents"])
        self.bridge_print_cross_generation_fluents(bridge_ir["cross_generation_fluents"])
        self.bridge_print_xgenerates(bridge_ir["xgenerates"])
        self.bridge_print_xinitiates(bridge_ir["xinitiates"])
        self.bridge_print_xterminates(bridge_ir["xterminates"])
        self.bridge_print_initials(bridge_ir["initials"])
        return self.out

    def instal_print(self, to_append: str) -> None:
        #Legacy. InstAL print used to print to file: it now just adds to an out variable which is returned.
        self.out += to_append + "\n"

    def bridge_print_standard_prelude(self) -> None:
        # Bridge rules - as in instalial compiler, the prelude is now in instal.models.InstalModel
        self.instal_print(bridge_prelude.format(**self.names))

    def bridge_print_constraints(self) -> None:
        pass

    def bridge_print_cross_initiation_fluents(self, ipows: list) -> None:
        # prints ipows
        for xf in ipows:
            sinst = self.names["source"]
            dinst = self.names["sink"]
            f = self.extendedterm2string(xf[1])
            fvars = {}
            self.collectVars(xf[1], fvars, compiler=self.sink_compiler)
            # TODO replace with fluent_rule_pattern
            self.instal_print("fluent(ipow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), inst({dinst}), sink({dinst}, {inst}), bridge({inst}), \n"
                              .format(f=f, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))
            # TODO replace with predicate_pattern
            for k in fvars:
                self.instal_print("   {pred}({tvar})," .format(pred=self.types[fvars[k]], tvar=k))

            # TODO replace with fluent pattern
            self.instal_print("    fluent({f}, {dinst})." .format(f=f, dinst=dinst))

            # TODO replace with ifluent rule pattern
            self.instal_print("ifluent(ipow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), inst({dinst}), sink({dinst}, {inst}), bridge({inst}), \n"
                              .format(f=f, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))

            # TODO replace with predicate_pattern
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]], tvar=k))
            ## TODO replace with fluent pattern
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))

    def bridge_print_cross_termination_fluents(self, tpows: list) -> None:
        # prints tpows
        for xf in tpows:
            sinst = self.names["source"]
            dinst = self.names["sink"]
            f = self.extendedterm2string(xf[1])
            fvars = {}
            self.collectVars(xf[1], fvars, compiler=self.sink_compiler)
            # TODO replace with fluent rule pattern
            self.instal_print("fluent(tpow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), inst({dinst}),"
                              " sink({dinst}, {inst}), bridge({inst}),"
                              .format(f=f, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))

            # TODO replace with predicate_pattern
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]], tvar=k))
            # TODO replace with fluent pattern
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))

            self.instal_print("ifluent(tpow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), "
                              "inst({dinst}), sink({dinst}, {inst}), bridge({inst}),"
                              .format(f=f, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))

            # TODO replace with predicate_pattern
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]], tvar=k))
            # TODO replace with fluent pattern
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))

    def bridge_print_cross_generation_fluents(self, gpows: list) -> None:
        # prints gpows
        for xf in gpows:
            sinst = self.names["source"]
            dinst = self.names["sink"]
            e = xf[1][0] + self.args2string(xf[1][1])
            te = self.typecheck(xf[1][1])

            # TODO replace with cross gen i? fluent rule pattern
            self.instal_print("fluent(gpow({sinst},{e},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), inst({dinst}), sink({dinst}, {inst}), bridge({inst}), \n"
                              "    event({e}), evinst({e}, {dinst}), evtype({e}, {dinst}, ex), {te}."
                              .format(e=e, te=te, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))
            self.instal_print("ifluent(gpow({sinst},{e},{dinst}), {inst}) :- \n"
                              "    inst({sinst}), source({sinst}, {inst}), inst({dinst}), sink({dinst}, {inst}), bridge({inst}), \n"
                              "    event({e}), evinst({e}, {dinst}), evtype({e}, {dinst}, ex), {te}."
                              .format(e=e, te=te, sinst=sinst, dinst=dinst, inst=self.names["bridge"]))

    def bridge_print_xgenerates(self, xgenerates: list) -> None:
        # generates
        self.instal_print("%\n% cross generate rules\n%")
        for rl in xgenerates:
            [inev, exev, cond, ti] = rl
            vars1 = {}
            self.collectVars(inev, vars1, compiler=self.source_compiler)
            self.collectVars(cond, vars1, compiler=self.source_compiler)
            if not ti:
                time = ""
            else:
                time = "+" + str(ti)
            for x in exev:
                vars2 = {}
                self.collectVars(x, vars2, compiler=self.sink_compiler)
                y = inev[0]
                if y == 'viol':
                    y = inev[1][0]
                sinst = self.names["source"]
                dinst = self.names["sink"]
                # TODO replace with cross_generate_rule_pattern
                self.instal_print(
                    "%\n"
                    "% Translation of {inev} of {sinst} xgenerates {x} of {dinst} if {condition} in {time}\n"
                    "occurred({x},{dinst},I{time}) :- occurred({inev},{sinst},I),\n"
                    "   holdsat(gpow({sinst},{x},{dinst}),{inst},I{time}), \n"
                    "    inst({sinst}), source({sinst}, {inst}), inst({dinst}), sink({dinst}, {inst}), bridge({inst}), \n"
                    .format(inev=self.extendedterm2string(inev),
                            x=self.extendedterm2string(x),
                            inst=self.names["bridge"],
                            sinst=sinst,
                            dinst=dinst,
                            condition=cond, time=time))
                self.printCondition(cond, sinst)
                # TODO replace with predicate pattern
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                # TODO replace with predicate pattern
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                # TODO replace with Instant pattern
                self.instal_print("instant(I).")

    def bridge_print_xinitiates(self, xinitiates: list) -> None:
        # initiates
        self.instal_print("%\n% cross initiation rules\n%")
        for rl in xinitiates:
            [sf, df, cond] = rl
            vars1 = {}
            self.collectVars(sf, vars1, compiler=self.source_compiler)
            self.collectVars(cond, vars1, compiler=self.source_compiler)
            for x in df:
                vars2 = {}
                self.collectVars(x, vars2, compiler=self.sink_compiler)
                y = sf[0]
                if y == 'viol':
                    y = sf[1][0]
                sinst = self.names["source"]
                dinst = self.names["sink"]

                self.instal_print(
                    "%\n% Translation of {sf} of {sinst} xinitiates {x} of {dinst} if {condition}"
                    .format(sf=self.extendedterm2string(sf), x=x, condition=cond, sinst=sinst, dinst=dinst))
                # TODO replace with xinitiate rule pattern
                self.instal_print("%\nxinitiated({sinst}, {x},{dinst},I) :-\n"
                                  "   occurred({sf},{sinst},I),\n"
                                  "   holdsat(ipow({sinst}, {x}, {dinst}), {inst}, I), \n"
                                  "   holdsat(live({inst}),{inst},I), bridge({inst}), \n"
                                  "   inst({dinst}), inst({sinst}), "
                                  .format(x=self.extendedterm2string(x),
                                          sf=self.extendedterm2string(sf),
                                          sinst=sinst,
                                          dinst=dinst,
                                          inst=self.names["bridge"]))
                self.printCondition(cond, sinst)
                # TODO replace with predicate pattern
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                # TODO replace with bridge pattern and instant pattern
                self.instal_print("   bridge({inst}), instant(I).".format(
                    inst=self.names["bridge"]))

    def bridge_print_xterminates(self, xterminates: list) -> None:
        # terminates
        self.instal_print("%\n% cross termination rules\n%")
        for rl in xterminates:
            [sf, df, cond] = rl
            vars1 = {}
            self.collectVars(sf, vars1, compiler=self.source_compiler)
            self.collectVars(cond, vars1, compiler=self.source_compiler)
            for x in df:
                vars2 = {}
                self.collectVars(x, vars2, compiler=self.sink_compiler)
                y = sf[0]
                if y == 'viol':
                    y = sf[1][0]
                sinst = self.names["source"]
                dinst = self.names["sink"]

                self.instal_print(
                    "%\n% Translation of {sf} of {sinst} xterminates {x} of {dinst} if {condition}"
                    .format(sf=self.extendedterm2string(sf), x=x, condition=cond, sinst=sinst, dinst=dinst))
                # TODO Replace with xterminate rule pattern
                self.instal_print("%\nxterminated({sinst}, {x},{dinst},I) :-\n"
                                  "   occurred({sf},{sinst},I),\n"
                                  "   holdsat(tpow({sinst}, {x}, {dinst}), {inst}, I), \n"
                                  "   holdsat(live({inst}),{inst},I), bridge({inst}), \n"
                                  "   inst({dinst}), inst({sinst}), "
                                  .format(x=self.extendedterm2string(x),
                                          sf=self.extendedterm2string(sf),
                                          sinst=sinst,
                                          dinst=dinst,
                                          inst=self.names["bridge"]))
                self.printCondition(cond, sinst)
                # TODO REplace with predicate pattern
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                # TODO replace with brdige / instant pattern
                self.instal_print("   bridge({inst}), instant(I).".format(
                    inst=self.names["bridge"]))

    def bridge_print_initials(self, initials: list) -> None:
        # TODO replace with bridge initial holdsat rule pattern
        self.instal_print("%\n% initially\n%")
        if True: # No creation events
            self.instal_print("% no creation event")
            self.instal_print("holdsat(live({bridge}),{bridge},I) :- start(I), bridge({bridge})."
                              .format(bridge=self.names["bridge"]))
            self.instal_print("holdsat(perm(null),{bridge},I) :- start(I), bridge({bridge})."
                              .format(bridge=self.names["bridge"]))
            for inits in initials:
                [i, cond] = inits
                fvars = {}
                self.instal_print("% initially: {x}"
                                  .format(x=self.extendedterm2string(i)))
                if not (cond == []):
                    self.instal_print(
                        "% condition: {x}"
                        .format(x=self.extendedterm2string(cond)))
                self.instal_print("holdsat({inf},{bridge},I) :- not holdsat(live({bridge}),{bridge}),"
                                  .format(bridge=self.names["bridge"],
                                          inf=self.extendedterm2string(i)))
                self.collectVars(i[1][1], fvars, compiler=self.sink_compiler)
                for k in fvars:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[fvars[k]], tvar=k))
                if not (cond == []):
                    self.printCondition(cond)
                self.instal_print(
                    "   bridge({bridge}), source({source}, {bridge}), sink({sink}, {bridge}), start(I).".format(**self.names))

    def collectVars(self, t, d, compiler: InstalCompiler=None):
        #As instalialcompiler. Needs to have a compiler argument because needs to use sink and/or source compilers.
        if compiler == self:
            return
        return compiler.collectVars(t, d)
