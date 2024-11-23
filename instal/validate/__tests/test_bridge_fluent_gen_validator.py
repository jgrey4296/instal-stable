#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from instal.validate.bridge_fluent_gen_validator import BridgeFluentGenValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM

logging = logmod.root
##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data

parser = InstalPyParser()

# TODO implemenet and test bridge fluent gen
class TestBridgeFluentGenValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ BridgeFluentGenValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_basic_pass(self):
        """
        Validator no reports are generated on proper use of events
        """
        file_name = data_path / "bridge_fluent_gen_rules.iab"
        runner    = validate.InstalValidatorRunner([ BridgeFluentGenValidator() ])

        data = parser.parse_bridge(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)