#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import json
import logging as logmod
import pathlib
import warnings
from clingo import Symbol
from clingo import parse_term as cpt
from instal.interfaces.solver import InstalModelResult
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from instal.trace.trace import InstalTrace


##-- data
data_path = files("instal.trace.__test.__data")
data_file = data_path / "trace_0.json"
data_text = data_file.read_text()
##-- end data


class TestTrace:

    def test_load_from_json(self):
        trace = InstalTrace.from_json(json.loads(data_text))
        assert(trace is not None)
        assert(len(trace) == 4)

    def test_build_from_model_three_events(self):
        model = InstalModelResult(atoms=[],
                                  shown=[cpt("occurred(something, 1)"),
                                         cpt("occurred(other, 2)"),
                                         cpt("occurred(else, 3)")],
                                  cost=1,
                                  number=1,
                                  optimal=False,
                                  type="test")
        trace = InstalTrace.from_model(model, steps=3)
        assert(len(trace) == 4)
        for state in trace:
            if state.timestep == 0:
                continue
            assert(state.occurred)

    def test_build_from_model_holdsat(self):
        model = InstalModelResult(atoms=[],
                                  shown=[cpt("holdsat(perm(something), 0)"),
                                         cpt("holdsat(perm(other), 0)"),
                                         cpt("holdsat(perm(else), 0)")],
                                  cost=1,
                                  number=1,
                                  optimal=False,
                                  type="test")

        trace = InstalTrace.from_model(model, steps=1)
        assert(len(trace) == 2)
        assert(len(trace[0].holdsat['perm']) == 3)


    def test_build_from_model_holdsat(self):
        model = InstalModelResult(atoms=[],
                                  shown=[cpt("observed(something, 1)"),
                                         cpt("observed(other, 1)"),
                                         cpt("observed(else, 2)")],
                                  cost=1,
                                  number=1,
                                  optimal=False,
                                  type="test")

        trace = InstalTrace.from_model(model, steps=2)
        assert(len(trace) == 3)
        assert(len(trace[1].observed) == 2)
        assert(len(trace[2].observed) == 1)



    def test_equivalence(self):
        """ Check a trace loads and saves without changing anything """
        trace = InstalTrace.from_json(json.loads(data_text))
        as_json = trace.to_json_str()

        reconstructed = as_json.split("\n")
        for orig, loaded in zip(data_text.split("\n"), reconstructed):
            with self.subTest(loaded):
                assert(orig == loaded)


    def test_filter(self):
        pass

    def test_fluent_intervals(self):
        pass

