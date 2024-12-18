#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
from importlib.resources import files
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest

from instal.validate.fluent_validator import FluentValidator
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


class TestFluentValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ FluentValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_basic_pass(self):
        """
        Validator there are no reports if a consistent institution is defined
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ FluentValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_initiate_fail(self):
        """
        Validator a report is generated if an inertial fluent isn't initiated anywhere.
        """
        file_name = data_path / "fluent_check_initiate_fail.ial"
        runner    = validate.InstalValidatorRunner([ FluentValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 1)
        assert(result[logmod.WARNING][0].msg == "Inertial Fluent Not Initiated Anywhere")

    def test_basic_terminate_fail(self):
        """
        Validator a report is generated if an inertial fluent isn't terminated anywhere
        """
        file_name = data_path / "fluent_check_terminate_fail.ial"
        runner    = validate.InstalValidatorRunner([ FluentValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 1)
        assert(result[logmod.WARNING][0].msg == "Inertial Fluent Not Terminated Anywhere")

    def test_basic_transient_fail(self):
        """
        a report is generated if a transient fluent isn't used as the head of a `when` rule.
        """
        file_name = data_path / "fluent_check_transient_fail.ial"
        runner    = validate.InstalValidatorRunner([ FluentValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 1)
        assert(result[logmod.WARNING][0].msg == "Transient Fluent Not Mentioned Anywhere")

    def test_success_on_consistent(self):
        file_name = data_path / "fluent_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ FluentValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_transient_initiation_fail(self):
        """
        report when a transient fluent is used like an inertial
        """
        pass

    def test_transient_termination_fail(self):
        """
        report when a transient fluent is used like an inertial
        """
        pass

