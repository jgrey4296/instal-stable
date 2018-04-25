from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserError


class TestXTerminatesBridge(InstalTestCase):
    inst1 = """
    institution inst1;
    type Alpha;
    exogenous event sourceExEvent;
    inst event sourceInstEvent;

    fluent sourceFlu1;
    fluent sourceFlu2(Alpha);
    fluent sourceFluOff;

    sourceExEvent generates sourceInstEvent;

    initially perm(sourceInstEvent), pow(sourceExEvent), perm(sourceExEvent);
    initially sourceFlu1, sourceFlu2(A);
    """

    inst2 = """
    institution inst2;

    type Alpha;

    exogenous event sinkExEvent;
    inst event sinkInstEvent;
    noninertial fluent sinkNoninertial;

    fluent sinkFluentWithArg(Alpha);
    fluent sinkFluent;

    initially perm(sinkInstEvent);

    initially sinkFluent, sinkFluentWithArg(A);
    """

    def test_xterminates_basic(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluent;

        cross fluent tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{
            "notholdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xterminates_notpow(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluent;

        cross fluent tpow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{
            "holdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xterminate_exevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkExEvent;

        cross fluent tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xterminate_inevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkInEvent;

        cross fluent tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xterminate_noninertial(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkNonInertial;

        cross fluent tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xterminate_withargs(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluentWithArg(a);

        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"notholdsat": ["holdsat(sinkFluentWithArg(a), inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xterminate_withargs_multiple(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluentWithArg(a), sinkFluent;

        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"notholdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                      "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xterminate_withargs_multiple_condition(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluentWithArg(a), sinkFluent if sourceFlu1;

        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"notholdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                      "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xterminate_withargs_multiple_condition_long(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluentWithArg(a), sinkFluent if sourceFlu1, sourceFlu2(a);

        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"notholdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                      "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xterminate_withargs_multiple_condition_off(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluentWithArg(a), sinkFluent if sourceFlu1, sourceFlu2(a), sourceFluOff;

        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially tpow(inst1, sinkFluent, inst2);
        initially tpow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                      "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)