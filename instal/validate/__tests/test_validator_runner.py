#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
from dataclasses import dataclass, field, InitVar
import warnings
import pathlib
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest

from instal.interfaces import validate
from instal.interfaces import ast as iAST
from instal.parser.v2.utils import TERM

logging = logmod.root

##-- util classes

@dataclass
class SimpleValidator(validate.InstalValidator_i):

    nodes : list = field(init=False, default_factory=list)

    def action_TermAST(self, visitor, node):
        self.nodes.append(node)

    def validate(self):
        match self.nodes[0].value:
            case "hardFail":
                raise Exception("told to hardFail")
            case "info report":
                self.delay_info("A Simple Report")
            case "warning":
                self.delay_warning("A Simple Warning")
            case _:
                self.delay_info(self.nodes[0].value)

@dataclass
class SecondValidator(validate.InstalValidator_i):

    def action_TermAST(self, visitor, node):
        self.delay_info("second validator fired")

##-- end util classes

class TestValidatorRunner:

    def test_initial(self):
        runner = validate.InstalValidatorRunner()
        assert(isinstance(runner, validate.InstalValidatorRunner))

    def test_initial_with_validator(self):
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_initial_failure(self):
        """
        Verify a validate throwing an error is recorded as level 101
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        with pytest.raises(Exception) as cm:
            runner.validate(iAST.TermAST("hardFail"))

        assert(cm.exception.args[1][101][0].args[0] == "told to hardFail")

    def test_simple_info_report(self):
        """
        Verify a validate reporting at INFO level is recorded
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        results = runner.validate(iAST.TermAST("info report"))
        assert(isinstance(results, dict))
        assert(logmod.INFO in results)
        assert(len(results[logmod.INFO]) == 1)
        assert(results[logmod.INFO][0].msg == "A Simple Report")

    def test_simple_warning_report(self):
        """
        Verify a validate reporting at WARNING level is recorded
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator() ])
        results = runner.validate(iAST.TermAST("warning"))
        assert(isinstance(results, dict))
        assert(logmod.WARNING in results)
        assert(len(results[logmod.WARNING]) == 1)
        assert(results[logmod.WARNING][0].msg == "A Simple Warning")

    def test_multi_validators(self):
        """
        Verify multiple validators can run without interference
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator(), SecondValidator() ])
        results = runner.validate(iAST.TermAST("blah"))
        assert(isinstance(results, dict))
        assert(logmod.INFO in results)
        assert(len(results[logmod.INFO]) == 2)
        msgs = [x.msg for x in results[logmod.INFO]]
        assert("blah" in msgs)
        assert("second validator fired" in msgs)

    def test_multi_validators_all_run(self):
        """
        Verify multiple validators can report at different levels
        """
        runner = validate.InstalValidatorRunner([ SimpleValidator(), SecondValidator() ])
        results = runner.validate(iAST.TermAST("warning"))
        assert(isinstance(results, dict))

        assert(logmod.INFO in results)
        assert(len(results[logmod.INFO]) == 1)
        msgs = [x.msg for x in results[logmod.INFO]]
        assert("second validator fired" in msgs)

        assert(logmod.WARN in results)
        assert(len(results[logmod.WARN]) == 1)
        assert(results[logmod.WARN][0].msg == "A Simple Warning")
