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
from instal.validate.name_duplication_validator import NameDuplicationValidator
from instal.parser.v2.parser import InstalPyParser
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.utils import TERM

logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
# data_file = data_path.joinpath("filename.ext")
# data_text = data_file.read_text()
##-- end data
parser = InstalPyParser()


class TestNameDuplicationValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_fluent_duplicate(self):
        """
        check an error report is raised when a fluent is duplicated
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert("Duplicate Fluent Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_event_duplicate(self):
        """
        check an event duplication report is generated
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert("Duplicate Event Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_event_conflict(self):
        """
        check an event-fluent conflict is recognized
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        assert(conflicts)

    def test_type_duplicate(self):
        """
        check a typedec duplication report is raised
        """
        test_file = data_path / "name_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert("Duplicate TypeDec Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_type_fluent_conflict(self):
        """
        check a typedec-fluent conflict report is raised
        """
        test_file = data_path / "type_fluent_conflict_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        assert(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        assert(iAST.FluentAST in asts)
        assert(iAST.DomainSpecAST in asts)



    def test_type_ex_event_conflict(self):
        """
        check typedec-event conflicts are recognized
        """
        test_file = data_path / "type_ex_event_conflict.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        assert(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        assert(iAST.EventAST in asts)
        assert(iAST.DomainSpecAST in asts)

    def test_type_inst_event_conflict(self):
        """
        check typedec-event conflicts are recognized
        """
        test_file = data_path / "type_inst_event_conflict.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        conflicts = [x for x in the_exc.args[1][logmod.ERROR] if x.msg == "Declaration Conflict"]
        assert(conflicts)
        asts = [conflicts[0].ast.__class__, conflicts[0].data.__class__]
        assert(iAST.EventAST in asts)
        assert(iAST.DomainSpecAST in asts)



    def test_fluent_duplication_with_params(self):
        """
        check exact fluent parameters can cause duplication reports
        """
        test_file = data_path / "name_params_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert(len(the_exc.args[1][logmod.ERROR]) == 1)
        assert("Duplicate Fluent Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})


    def test_fluent_duplication_with_vars(self):
        """
        check fluents with the same variables trigger duplication reports
        """
        test_file = data_path / "name_vars_duplication_test.ial"
        runner    = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        data      = parser.parse_institution(test_file)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert("Duplicate Fluent Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})

    def test_fluent_duplication_with_numbered_vars(self):
        """
        check fluent declaration with vars only differing by index number
        generate duplication reports
        """
        runner = validate.InstalValidatorRunner([ NameDuplicationValidator() ])
        file_name = data_path / "name_vars_numbered_duplication_test.ial"
        data = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            runner.validate(data)

        the_exc = cm.exception
        assert(logmod.ERROR in the_exc.args[1])
        assert(the_exc.args[1][logmod.ERROR])
        assert("Duplicate Fluent Declaration" in {x.msg for x in the_exc.args[1][logmod.ERROR]})
