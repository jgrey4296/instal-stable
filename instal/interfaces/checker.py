#/usr/bin/env python3
"""
The Interface for running compile time sanity checks on an instal model
"""
##-- imports
from __future__ import annotations

import warnings
import abc
import logging as logmod
from collections import defaultdict
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

from instal.interfaces.ast import InstalAST

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports


logging = logmod.getLogger(__name__)


@dataclass
class InstalCheckReport:
    """
    A Result of an InstalCheck.

    """
    ast     : InstalAST       = field()
    msg     : str             = field()
    level   : int             = field(kw_only=True)
    checker : InstalChecker_i = field(kw_only=True)
    source  : str             = field(kw_only=True)

    fmt     : str             = field(kw_only=True, default="({level}) Source: {source} : {msg}")

    def __str__(self):
        return self.fmt.format_map({"msg"    :self.msg,
                                    "level"  :self.level,
                                    "source" :self.source or "No File"})

@dataclass
class InstalChecker_i(metaclass=abc.ABCMeta):
    """
    The Core Interface for running compile time checks
    on an instal specification.

    parsers return list[InstalAST],
    so a checker takes a heterogenous collection of InstalAST's,
    and checks they make sense
    """

    current_reports : list[InstalCheckReport] = field(init=False, default_factory=list)

    def clear(self):
        self.current_reports = []

    def debug(self, msg, ast=None):
        self.build_note(ast, msg, logmod.DEBUG)

    def info(self, msg, ast=None):
        self.build_note(ast, msg, logmod.INFO)

    def warning(self, msg, ast=None):
        self.build_note(ast, msg, logmod.WARN)

    def error(self, msg, ast=None):
        self.build_note(ast, msg, logmod.ERROR)

    def build_note(self, ast, msg, level):
        self.current_reports.append(InstalCheckReport(ast, msg,
                                                      level=level,
                                                      checker=self.__class__,
                                                      source=ast.sources_str if hasattr(ast, 'sources_str') else "No Source File"))

    def __call__(self, asts:list[InstalAST]) -> list[InstalCheckReport]:
        assert(isinstance(asts, list))
        self.clear()
        self.check(asts)
        return self.current_reports[:]

    @abc.abstractmethod
    def check(self, asts:list[InstalAST]): pass



class InstalExtractor_i(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def extract(self, asts:list[InstalAST]) -> list[InstalAST]: pass

@dataclass
class InstalCheckRunner:
    """
    Given a collection of Instal Checkers,
    and a list of InstalAST's,
    runs the checkers on the ast's
    and warns / errors / reports a collection of results
    """

    components : list[InstalChecker_i | InstalExtractor_i] = field(default_factory=list)

    checkers   : list[InstalChecker_i]   = field(init=False, default_factory=list)
    extractors : list[InstalExtractor_i] = field(init=False, default_factory=list)

    def __post_init__(self):
        for comp in self.components:
            if isinstance(comp, InstalChecker_i):
                self.checkers.append(comp)
            if isinstance(comp, InstalExtractor_i) or hasattr(comp, 'extract'):
                self.extractors.append(comp)

        logging.info("%s built with %s extractors and %s checkers",
                     self.__class__.__name__,
                     len(self.extractors),
                     len(self.checkers))

    def check(self, asts:list[InstalAST]) -> list[InstalCheckReport]:
        if not isinstance(asts, list):
            asts = [asts]
        logging.info("Running Check on %s primary level asts", len(asts))
        total_results                = defaultdict(lambda: [])
        hard_fails : list[Exception] = []
        error_count : int            = 0

        # Run extractors to flatten as necessary
        extracted_asts = asts[:]
        for extractor in self.extractors:
            logging.debug("Running Extractor: %s", extractor.__class__.__name__)
            extracted_asts += extractor.extract(asts)

        for checker in self.checkers:
            logging.debug("Running Checker: %s", checker.__class__.__name__)
            # Run the Check, recording results
            try:
                results = checker(extracted_asts)
                # Collect the reports by level
                for note in results:
                    total_results[note.level].append(note)
                    error_count += 1 if note.level >= logmod.ERROR else 0

            except Exception as err:
                hard_fails.append(err)
                error_count += 1

        # When all checks are done, report exceptions
        if bool(error_count):
            just_errors = {x:y for x,y in total_results.items() if x >= logmod.ERROR}
            just_errors.update({101:hard_fails})
            raise Exception(f"Checking produced {error_count} errors", just_errors)

        # warning if theres any
        warnings = [report for x,y in total_results.items() for report in y if logmod.INFO < x <= logmod.ERROR]
        for report in sorted(warnings, key=lambda x:x.level):
            logging.warning(str(report))

        return total_results
