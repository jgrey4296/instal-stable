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
from instal.validate.event_validator import EventValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM
##-- end imports

logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
##
parser = InstalPyParser()

class TestEventValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ EventValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_basic_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "event_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_inst_fail(self):
        """
        a report is generated if an institutional event is not generated
        """
        file_name = data_path / "event_check_inst_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(len(result[logmod.WARNING]) == 1)
        assert(result[logmod.WARNING][0].msg == "Institutional Event is not generated")

    def test_basic_chain_pass(self):
        """
        reports aren't generated when institutional events generate
        further institutional events
        """
        file_name = data_path / "event_check_chain_pass.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_ex_fail(self):
        """
        a report is generated if an external event is not used
        """
        file_name = data_path / "event_check_ex_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(len(result[logmod.WARNING]) == 1)
        assert(result[logmod.WARNING][0].msg == "Unused External Event")



    def test_basic_fail_detail(self):
        """
        Check appropriate details of a report
        """
        file_name = data_path / "event_check_fail.ial"
        runner    = validate.InstalValidatorRunner([ EventValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 2)
        msgs = [x.msg for x in result[logmod.WARNING]]
        assert("Unused External Event" in msgs)
        assert("Institutional Event is not generated" in msgs)
