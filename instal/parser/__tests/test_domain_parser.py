#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import unittest
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.parser.pyparse_institution import InstalPyParser
from instal.interfaces.ast import DomainTotalityAST
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

class TestDomainParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)

        cls.dsl = InstalPyParser()


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_simple_domain_spec(self):
        result = self.dsl.parse_domain("Agent: alice")
        self.assertIsInstance(result, DomainTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result.body[0].terms), 1)
        self.assertEqual(result.body[0].head.value, "Agent")
        self.assertEqual(result.body[0].terms[0].value, "alice")

    def test_multi_instance_domain_spec(self):
        result = self.dsl.parse_domain("Agent: alice bob")
        self.assertIsInstance(result, DomainTotalityAST)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.body[0].head.value, "Agent")
        values = {x.value for x in result.body[0].terms}
        self.assertEqual(values, {"alice", "bob"})

    def test_multi_type_domain_spec(self):
        result = self.dsl.parse_domain("Agent: alice bob\nBook: book1 book2")
        self.assertIsInstance(result, DomainTotalityAST)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.body[0].head.value, "Agent")
        self.assertEqual(result.body[1].head.value, "Book")





if __name__ == '__main__':
    unittest.main()
