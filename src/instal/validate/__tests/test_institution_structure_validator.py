#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import warnings
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
##-- end imports

import pytest
from instal.validate.institution_structure_validator import \
    InstitutionStructureValidator
from instal.interfaces import ast as iAST
from instal.interfaces import validate
from instal.parser.v2.utils import TERM


logging = logmod.root


class TestInstitutionStructureValidator:

    def test_initial_ctor_with_validator(self):
        runner = validate.InstalValidatorRunner([ InstitutionStructureValidator() ])
        assert(isinstance(runner, validate.InstalValidatorRunner))
        assert(runner.validators is not None)

    def test_basic_validator_run(self):
        " Run a simple validate on an empty institution. "
        runner = validate.InstalValidatorRunner([ InstitutionStructureValidator() ])

        basic_inst = iAST.InstitutionDefAST(TERM.parse_string("test_inst")[0])

        results = runner.validate([basic_inst])
        # Provides warnings about the fluents,events,types,rules and facts being empty:
        assert(logmod.WARNING in results)
        assert(results[logmod.WARNING])
        assert(len(results[logmod.WARNING]) == 5)
