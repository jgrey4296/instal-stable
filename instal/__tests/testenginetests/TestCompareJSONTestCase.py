from instal.firstprinciples.TestEngine import InstalTestCase, InstalCompareJSONTestCase


class CompareJSONEngine(InstalTestCase):

    def test_compare_two_json(self):

        test_runner = InstalCompareJSONTestCase(
            self.CORRECT_JSON, self.CORRECT_JSON)

        test_runner.run_test()

    def test_compare_two_fail(self):

        test_runner = InstalCompareJSONTestCase(
            self.CORRECT_JSON, self.WRONG_JSON)

        with self.assertRaises(AssertionError):
            test_runner.run_test()

    def setUp(self):
        self.CORRECT_JSON = open("testenginetests/correct.json", "rt")
        self.WRONG_JSON = open("testenginetests/wrong.json", "rt")
