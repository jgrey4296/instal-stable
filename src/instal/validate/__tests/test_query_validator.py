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
from instal.validate.query_validator import QueryValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM


logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
parser = InstalPyParser()

class TestQueryValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ QueryValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_trivial_pass(self):
        """
        Validator no reports are generated on proper use of events
        """
        file_name = data_path / "basic_empty_inst.ial"
        runner    = validate.InstalValidatorRunner([ QueryValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)

    def test_basic_pass(self):
        """
        Validator no reports are generated on proper use of events
        """
        inst_file_name  = data_path / "basic_query_inst.ial"
        query_file_name = data_path / "basic_query_pass.iaq"
        runner          = validate.InstalValidatorRunner([ QueryValidator() ])
        inst_data       = parser.parse_institution(inst_file_name)
        query_data      = parser.parse_query(query_file_name)
        assert(isinstance(inst_data[0], iAST.InstitutionDefAST))
        assert(isinstance(query_data[0], iAST.QueryAST))

        result = runner.validate(inst_data + query_data)
        assert(not result)


    def test_basic_fail(self):
        """
        check reports are generated on unse of unrecognized events
        """
        inst_file_name  = data_path / "basic_query_inst.ial"
        query_file_name = data_path / "basic_query_fail.iaq"
        runner          = validate.InstalValidatorRunner([ QueryValidator() ])
        inst_data       = parser.parse_institution(inst_file_name)
        query_data      = parser.parse_query(query_file_name)
        assert(isinstance(inst_data[0], iAST.InstitutionDefAST))
        assert(isinstance(query_data[0], iAST.QueryAST))

        with self.assertRaises(Exception) as cm:
            runner.validate(inst_data + query_data)

        the_exc = cm.exception
        results = the_exc.args[1]
        assert(results)
        assert(logmod.ERROR in results)
