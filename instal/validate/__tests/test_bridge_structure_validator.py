
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
from instal.validate.bridge_structure_validator import BridgeStructureValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM

##-- end imports

logging = logmod.root
##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data

parser = InstalPyParser()

class TestBridgeStructureValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ BridgeStructureValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_basic_pass(self):
        """
        Validator a basic bridge + source + sink doesn't report
        """
        bridge_file_name = data_path / "bridge_structure_basic.iab"
        insts_file_name  = data_path / "bridge_structure_insts.ial"
        runner           = validate.InstalValidatorRunner([ BridgeStructureValidator() ])

        bridge_data = parser.parse_bridge(bridge_file_name)
        insts_data  = parser.parse_institution(insts_file_name)

        assert(len(bridge_data) == 1)
        assert(len(insts_data) == 2)

        result = runner.validate(bridge_data + insts_data)
        assert(not result)

    def test_basic_fail(self):
        """
        Validator a basic bridge + source + sink doesn't report
        """
        bridge_file_name = data_path / "bridge_structure_basic.iab"
        runner           = validate.InstalValidatorRunner([ BridgeStructureValidator() ])

        bridge_data = parser.parse_bridge(bridge_file_name)

        assert(len(bridge_data) == 1)

        result = runner.validate(bridge_data)
        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 2)
        msgs = {x.msg for x in result[logmod.WARNING]}
        assert("Bridge Source declared but not defined" in msgs)
        assert("Bridge Sink declared but not defined" in msgs)
