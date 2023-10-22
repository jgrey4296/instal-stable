#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
from importlib.resources import files
from instal.parser.v2.parser import InstalPyParser

import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.utils import TERM
from instal.validate.declaration_type_validator import DeclarationTypeValidator

logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
parser = InstalPyParser()


# TODO implement and test declaration types
class TestDeclarationTypeValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_empty_pass(self):
        """
        no reports are generated on an empty inst
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "term_type_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    @pytest.mark.xfail
    def test_basic_fail(self):
        """
        reports are generated on type conflicts
        """
        file_name = data_path / "term_type_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeclarationTypeValidator() ])

        text = data_path.joinpath(file_name).read_text()
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(result)
