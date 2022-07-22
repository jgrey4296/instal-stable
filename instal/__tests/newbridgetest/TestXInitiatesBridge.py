from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserError


class TestXInitiatesBridge(InstalTestCase):
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
    """

    def test_xinitiate_basic(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"holdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xinitiate_noipow(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"notholdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xinitiate_exevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkExEvent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_inevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkInEvent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_noninertial(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkNonInertial;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_withargs(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a);

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xinitiate_multiple(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a), sinkFluent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                   "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xinitiate_multiple_condition(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a), sinkFluent if sourceFlu1;

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                   "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)

    def test_xinitiate_multiple_condition_long(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a), sinkFluent if sourceFlu1, sourceFlu2(a);

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                   "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose, conditions=conditions)

    def test_xinitiate_multiple_condition_off(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a), sinkFluent if sourceFlu1, sourceFlu2(a), sourceFluOff;

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"notholdsat": ["holdsat(sinkFluentWithArg(a), inst2)",
                                   "holdsat(sinkFluent, inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose, conditions=conditions)