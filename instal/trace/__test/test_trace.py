#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import json
import logging as logmod
import pathlib
import unittest
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.trace.trace import InstalTrace
##-- end imports

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings

##-- data
data_path = files("instal.trace.__test")
data_file = data_path / "trace_0.json"
data_text = data_file.read_text()
##-- end data


class TestTrace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.getLogger(__name__)
        logging.root.addHandler(cls.file_h)
        logging.root.setLevel(logmod.NOTSET)


    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)

    def test_initial(self):
        trace = InstalTrace.from_json(json.loads(data_text))
        self.assertIsNotNone(trace)
        self.assertEqual(len(trace), 4)

    def test_equivalence(self):
        """ Check a trace loads and saves without changing anything """
        trace = InstalTrace.from_json(json.loads(data_text))
        as_json = json.dumps(trace.to_json(), sort_keys=True, indent=4)

        reconstructed = as_json.split("\n")
        for orig, loaded in zip(data_text.split("\n"), reconstructed):
            with self.subTest(loaded):
                self.assertEqual(orig, loaded)

if __name__ == '__main__':
    unittest.main()
