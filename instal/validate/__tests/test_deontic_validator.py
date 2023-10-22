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
from instal.validate.deontic_validator import DeonticValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM

logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
parser = InstalPyParser()

class TestDeonticValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ DeonticValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_empty_pass(self):
        """
        check no reports are generated on an empty institution
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_fail(self):
        """
        check reports are generated on improper use of deontics
        """
        file_name = data_path / "deontic_check_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])

        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(the_exc.args[1])
        assert(len(the_exc.args[1][40]) == 2)

        bad_asts = {x.ast.params[0].signature for x in the_exc.args[1][40]}
        assert(bad_asts == set(["aFluent/0", "testEvent/0"]))

    def test_basic_pass(self):
        """
        check no reports are generated on deontics applied to institutional events
        """
        file_name = data_path / "deontic_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_obligation_fluent_name_duplication_fail(self):
        """

        """
        file_name = data_path / "obl_deontic_name_duplication_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))
        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(the_exc.args)
        assert(len(the_exc.args[1][40]) == 2)
        msgs = [x.msg for x in the_exc.args[1][40]]
        assert("Duplicate obligation declared" in msgs)
        assert("Obligation Use does not match Declaration" in msgs)

    def test_obligation_fluent_structure_fail(self):
        """

        """
        file_name = data_path / "obl_deontic_check_structure_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))
        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(the_exc.args)
        assert(len(the_exc.args[1][40]) == 1)
        msg = the_exc.args[1][40][0].msg
        assert(msg == "Obligation Use does not match Declaration")

    def test_obligation_fluent_def_fail(self):
        """
        Report on obligations not using institutional events as parameters
        """
        file_name = data_path / "obl_deontic_check_def_fail.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))
        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(the_exc.args)
        assert(len(the_exc.args[1][40]) == 1)
        msg = the_exc.args[1][40][0].msg
        assert(msg == "Obligation Declared with an incompatiable argument")

    def test_obligation_fluent_pass(self):
        """

        """
        file_name = data_path / "obl_deontic_check_pass.ial"
        runner    = validate.InstalValidatorRunner([ DeonticValidator() ])
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)
