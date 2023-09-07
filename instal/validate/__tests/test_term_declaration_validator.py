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
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.parser import InstalPyParser
from instal.parser.v2.utils import TERM
from instal.validate.term_declaration_validator import TermDeclarationValidator

logging = logmod.root

##-- data
data_path = files("instal.validate.__tests.__data")
##-- end data
parser = InstalPyParser()


class TestTermDeclarationValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)


    def test_basic_use_fail(self):
        """
        an error report is generated for term use without declaration
        """
        file_name = data_path / "term_decl_use_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            result = runner.validate(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        assert(len(result[logmod.ERROR]) == 1)
        assert(result[logmod.ERROR][0].msg == "Term used without declaration")
        assert(str(result[logmod.ERROR][0].ast) == "badEv")


    def test_basic_signature_fail(self):
        """
        an error report is generated for signature mismatches
        """
        file_name = data_path / "term_decl_signature_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        with pytest.raises(Exception) as cm:
            result = runner.validate(data)

        the_exc = cm.exception
        result = the_exc.args[1]
        assert(len(result[logmod.ERROR]) == 1)
        assert(result[logmod.ERROR][0].msg == "Term used without declaration, but these were: [ simpleEv/0 ]")
        assert(str(result[logmod.ERROR][0].ast) == "simpleEv(TestVar)")


    def test_type_declaration_usage_pass(self):
        """
        no reports are generated on proper use of events
        """
        file_name = data_path / "term_decl_pass.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)
        assert(not result)


    def test_type_declaration_usage_fail(self):
        """
        a report is generated for declarations that aren't used
        """
        file_name = data_path / "term_decl_fail.ial"
        runner    = validate.InstalValidatorRunner([ TermDeclarationValidator() ])
        data      = parser.parse_institution(file_name)
        assert(isinstance(data[0], iAST.InstitutionDefAST))

        result = runner.validate(data)

        assert(result)
        assert(logmod.WARNING in result)
        assert(len(result[logmod.WARNING]) == 1)
        msgs = {x.msg for x in result[logmod.WARNING]}
        assert(len(msgs) == 1)
        assert("Term declared without use" in msgs)
        assert(repr(result[logmod.WARNING][0].ast.head) == "Other")
