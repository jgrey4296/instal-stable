from instal.firstprinciples.TestEngine import InstalTestCase, InstalSingleShotTestRunnerFromText
from instal.instalexceptions import InstalParserTypeError
class Occurs(InstalTestCase):
    BASE_IAL = """
        institution non;

        noninertial fluent a;
        noninertial fluent b;
        noninertial fluent c;
        noninertial fluent d;
        noninertial fluent e;
    """
    def test_occurs_basic(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when a;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])

    def test_occurs_basic_not(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when not a;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])

    def test_occurs_basic_ok(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when b;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])

    def test_occurs_transitive(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when b; b when a;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])

    def test_occurs_transitive_chain(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when b; b when c; c when d; d when a;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])


    def test_occurs_transitive_chain_not(self):
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.BASE_IAL+"a when b; b when not c; c when d; d when not a;"], bridge_file=[],
                                                    domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                        conditions=[])

    def test_occurs_basic_with_multiple(self):
        runner = InstalSingleShotTestRunnerFromText(
            input_files=[self.BASE_IAL + "a when a,b;"], bridge_file=[],
            domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                            conditions=[])

    def test_occurs_transitive_with_multiple(self):
        runner = InstalSingleShotTestRunnerFromText(
            input_files=[self.BASE_IAL + "a when b, c; c when a;"], bridge_file=[],
            domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                            conditions=[])

    def test_occurs_chain_with_multiple(self):
        runner = InstalSingleShotTestRunnerFromText(
            input_files=[self.BASE_IAL + "a when b, c; c when d; d when a;"], bridge_file=[],
            domain_files=[], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="noninertials/null.iaq", verbose=self.verbose,
                            conditions=[])