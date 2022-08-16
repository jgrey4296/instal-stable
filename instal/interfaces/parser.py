##-- imports
from __future__ import annotations

import abc
import logging as logmod
import pathlib
from importlib.readers import MultiplexedPath
from types import NoneType
from typing import IO, List
from unittest import TestCase, skip

import instal.interfaces.ast as InASTs
import pyparsing as pp
import pyparsing.testing as ppt
from instal.util.misc import InstalFileGroup

##-- end imports

logging = logmod.getLogger(__name__)

class InstalParser(metaclass=abc.ABCMeta):
    """
        InstalParserWrapper
        See __init__.py for more details.
    """

    def parse(self, file_group:InstalFileGroup) -> InASTs.ModelAST:
        """
        Read and parse multiple instal files into the AST representation
        *Only* handles the institutions and bridges,
        *Not* domains, facts or queries
        """
        try:
            text : str = ""
            ir_program : InASTs.InstalAST = InASTs.ModelAST()
            for path in file_group.institutions:
                with open(path, 'r') as f:
                    text = f.read()
                ir : InASTs.InstalAST = self.parse_institution(text)
                ir_program.institutions.append(ir)

            for path in file_group.bridges:
                with open(path, 'r') as f:
                    text = f.read()
                ir : InASTs.InstalAST = self.parse_bridge(text, ir_program.institutions)
                ir_program.bridges.append(ir)

        except FileNotFoundError as err:
            logging.exception("File Not Found for Parsing: %s", path)

        return ir_program

    @abc.abstractmethod
    def parse_institution(self, text:str) -> InASTs.InstalAST: pass
    @abc.abstractmethod
    def parse_bridge(self, text:str) -> InASTs.InstalAST: pass
    @abc.abstractmethod
    def parse_domain(self, text:str) -> list[InASTs.InstalAST]: pass
    @abc.abstractmethod
    def parse_situation(self, text:str) -> list[InASTs.InstalAST]: pass
    @abc.abstractmethod
    def parse_query(self, text:str) -> list[InASTs.InstalAST]: pass




class InstalParserTestCase(TestCase):

    current_parse_text : None|str = None

    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)


    def assertFilesParse(self, dsl:pp.ParserElement, *files:str|pathlib.Path, loc:None|MultiPlexedPath=None):
        """
        Assert all files parse.
        Can be simple names all appended to the path `loc` if provided,
        which is expected to be a MultiplexedPath provided by
        importlib.resources.files
        """
        self.assertIsInstance(dsl, pp.ParserElement)
        self.assertTrue(isinstance(loc, (NoneType, MultiplexedPath)))
        file_paths = (pathlib.Path(path) for path in files)
        file_locs  = (loc / path for path in file_paths) if loc is not None else file_paths

        for path in file_locs:
            with self.subTest(msg=path):
                self.assertTrue(path.exists())
                try:
                    result   = dsl.parse_file(path, parse_all=True)
                except pp.ParseException as err:
                    raise self.failureException("\n"+err.explain(0)) from None

    def yieldParseResults(self, dsl:pp.ParserElement, *tests) -> Iterator:
        """
        For each test, yield its result and additional values
        for manual testing
        """
        for test in tests:
            text, data = None, None
            self.assertIsInstance(test, (str, tuple, dict))
            match test:
                case str():
                    text = test
                    data = None
                case tuple():
                    text = test[0]
                    data = test
                case dict():
                    self.assertIn("text", test)
                    text = test['text']
                    data = test
                case _:
                    self.failureException("Test passed to yieldParseResults is confusing: %s", test)

            self._set_current_parse_text(text)
            try:
                result   = dsl.parse_string(text, parse_all=True)
            except pp.ParseException as err:
                raise self.failureException("\n"+err.explain(0)) from None

            yield result, data

        self._clear_current_parse_text()

    def assertParseResults(self, dsl:pp.ParserElement, *tests):
        """
        Run Tests of definition (testStr, {namedresults}?, listResults...)
        """
        self.assertIsInstance(dsl, pp.ParserElement)
        for test in tests:
            self.assertIsInstance(test, tuple, test[0])
            self.assertGreaterEqual(len(test), 2, test[0])
            with self.subTest(msg=test[0]):
                try:
                    result   = dsl.parse_string(test[0], parse_all=True)
                except pp.ParseException as err:
                    raise self.failureException("\n"+err.explain(0)) from None

                named    = test[1] if isinstance(test[1], dict) else {}
                expected = test[1 if not bool(named) else 2:]

                for x,y in named.items():
                    self.assertIn(x, result, test[0])
                    self.assertEqual(result[x], y, test[0])

                self.assertEqual(len(result), len(expected), test[0])
                for x,y in zip(result, expected):
                    self.assertEqual(x, y, test[0])


    def assertParseResultsIsInstance(self, dsl:pp.ParserElement, *tests):
        """
        Run Tests of definition (testStr, {namedresults}?, listResults...)
        """
        self.assertIsInstance(dsl, pp.ParserElement)
        for test in tests:
            self.assertIsInstance(test, tuple)
            self.assertGreaterEqual(len(test), 2)
            with self.subTest(test[0]):
                result   = dsl.parse_string(test[0], parse_all=True)
                expected = test[1:]
                self.assertEqual(len(result), len(expected))
                self.assertTrue(all(isinstance(x, type) for x in expected))

                for x,y in zip(result, expected):
                    self.assertIsInstance(x, y)

    def assertParserFails(self, dsl:pp.ParserElement, *tests):
        """
        Run Tests expected to fail: (testStr, failLoc)
        """
        self.assertIsInstance(dsl, pp.ParserElement)
        for test in tests:
            with self.subTest(test[0]):
                fail_loc = test[1]
                test_exc = test[2] if len(test) > 2 else pp.ParseException
                self.assertIsInstance(fail_loc, int)
                self.assertLess(fail_loc, len(test[0]))

                with self.assertRaises(test_exc) as cm:
                    dsl.parse_string(test[0], parse_all=True)

                exc = cm.exception
                self.assertEqual(exc.loc, fail_loc,
                                 "\n"+exc.explain(0))


    def assertAllIn(self, values, container):
        for value in values:
            self.assertIn(value, container)
    def _formatMessage(self, msg, standardMsg):
        """Honour the longMessage attribute when generating failure messages.
        If longMessage is False this means:
        * Use only an explicit message if it is provided
        * Otherwise use the standard message for the assert

        If longMessage is True:
        * Use the standard message
        * If an explicit message is provided, plus ' : ' and the explicit message
        """
        if not self.longMessage:
            return msg or standardMsg
        if msg is None and self.current_parse_text is None:
            return standardMsg
        if msg is None and self.current_parse_text is not None:
            return standardMsg + f'\n\n in:\n{self.current_parse_text}'
        try:
            # don't switch to '{}' formatting in Python 2.X
            # it changes the way unicode input is handled
            if self.current_parse_text:
                return '%s : %s\n\nin:\n%s' % (standardMsg, msg, self.current_parse_text)
            else:
                return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            if self.current_parse_text is not None:
                return  '%s : %s\n\nin:\n%s' % (safe_repr(standardMsg), safe_repr(msg), safe_repr(self.current_parse_text))
            else:
                return  '%s : %s' % (safe_repr(standardMsg), safe_repr(msg or self.current_parse_text))


    def _set_current_parse_text(self, text:str):
        as_lines = text.split("\n")
        rejoined = "\n".join(x.strip() for x in as_lines)
        self.current_parse_text = f'"{rejoined}"\n(ws trimmed)'

    def _clear_current_parse_text(self):
        self.current_parse_text = None
