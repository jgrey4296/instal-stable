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
from instal.interfaces.util import InstalASTVisitor_i

from instal.util.generated_visitor import InstalBaseASTVisitor
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
    data    : Any             = field(kw_only=True, default=None)

    fmt     : str             = field(kw_only=True, default="({level}) {source}{loc} {msg}")

    def __repr__(self):
        return str(self) + f" AST: {self.ast}"

    def __str__(self):
        loc    = ""
        source = ""
        if self.ast and bool(self.ast.parse_source):
            source = f"Source: {self.ast.parse_source[0]}: "

        if self.ast and self.ast.parse_loc is not None:
            loc = f"L:{self.ast.parse_loc[0]}, C:{self.ast.parse_loc[1]}: "

        return self.fmt.format_map({"msg"    : self.msg,
                                    "level"  : logmod.getLevelName(self.level),
                                    "source" : source,
                                    "loc"    : loc})

@dataclass
class InstalChecker_i(metaclass=abc.ABCMeta):
    """
    The Core Interface for running compile time checks
    on an instal specification.

    parsers return list[InstalAST],

    the check runner triggers an AST walk, which a checker will
    have registered actions on with `get_actions`

    then `check` is called, and any data the checker's actions have stored
    will be used to generate reports

    NOTE: checkers use an internal trio of debug/info/warning methods
    instead of just logging, or raising an error,
    so that *all* checks can be run, instead of throwing up to the runner on the first error.

    """

    current_reports : list[InstalCheckReport] = field(init=False, default_factory=list)

    def get_actions(self) -> dict:
        """
        return a dictionary of visit actions for addition to the check walker
        """
        return {}

    def clear(self):
        """
        A Clear method for implementations to use
        """
        pass

    def full_clear(self):
        """
        The full clear triggered by the check runner
        """
        self.current_reports = []
        self.clear()

    def debug(self, msg, ast=None, data=None):
        self.build_note(ast, msg, logmod.DEBUG, data)

    def info(self, msg, ast=None, data=None):
        self.build_note(ast, msg, logmod.INFO, data)

    def warning(self, msg, ast=None, data=None):
        self.build_note(ast, msg, logmod.WARN, data)

    def error(self, msg, ast=None, data=None):
        self.build_note(ast, msg, logmod.ERROR, data)

    def build_note(self, ast, msg, level, data):
        self.current_reports.append(InstalCheckReport(ast, msg,
                                                      level=level,
                                                      checker=self.__class__,
                                                      data=data))


    def __call__(self) -> list[InstalCheckReport]:
        """
        The access point used by InstalCheckRunner.
        Clears the log of reports generated, runs the .check method,
        and returns the new list of reports.
        """
        self.check()
        return self.current_reports[:]

    def check(self):
        pass



@dataclass
class InstalCheckRunner:
    """
    Given a collection of Instal Checkers,
    and a list of InstalAST's,
    runs the checkers on the ast's
    and warns / errors / reports a collection of results
    """

    checkers : list[InstalChecker_i] = field(default_factory=list)
    visitor  : InstalASTVisitor_i    = field(default_factory=InstalBaseASTVisitor)

    def __post_init__(self):
        # Register all checkers' actions with the visitor
        for comp in self.checkers:
            self.visitor.add_actions(comp.get_actions())


        logging.info("%s built with %s checkers and visitor class %s",
                     self.__class__.__name__,
                     len(self.checkers),
                     self.visitor.__class__.__name__)

    def check(self, asts:list[InstalAST]) -> list[InstalCheckReport]:
        if not isinstance(asts, list):
            asts = [asts]
        logging.info("Running Check on %s primary level asts", len(asts))
        total_results                = defaultdict(lambda: [])
        hard_fails : list[Exception] = []
        error_count : int            = 0

        for checker in self.checkers:
            checker.clear()


        logging.debug("Visiting nodes")
        self.visitor.visit_all(asts)


        for checker in self.checkers:
            logging.debug("Running Checker: %s", checker.__class__.__name__)
            # Run the Check, recording results
            try:
                results = checker()
                # Collect the reports by level
                for note in results:
                    total_results[note.level].append(note)
                    error_count += 1 if note.level >= logmod.ERROR else 0

            except Exception as err:
                # If a checker actually *errors*, record that but keep going
                logging.exception("Checker Hard Failed: %s", checker)
                hard_fails.append(err)
                error_count += 1

        # When all checks are done, report exceptions
        if bool(error_count):
            just_errors = {x:y for x,y in total_results.items() if x >= logmod.ERROR}
            just_errors.update({101:hard_fails})
            raise Exception(f"Checking produced Errors: {error_count}", just_errors)

        # warning if theres any
        warnings = [report for x,y in total_results.items() for report in y if logmod.INFO < x <= logmod.ERROR]
        for report in sorted(warnings, key=lambda x:x.level):
            logging.warning(str(report))

        return dict(total_results)
