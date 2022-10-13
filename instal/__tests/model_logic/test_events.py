#!/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

#
import logging as logmod
import pathlib
import unittest
import warnings
from importlib.resources import files
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from unittest import mock

from instal.cli.compiler import compile_target
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.parser.v2.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver

##-- end imports

##-- data
test_files      = files("instal.__data.test_files.minimal")
##-- end data

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root


def save_last(compiled, append=None):
    "A utility to save lines of text to a file for debugging compiled output "
    with open(pathlib.Path(__file__).parent / "last_run.lp", 'w') as f:
        f.write("\n".join(compiled))
        if bool(append):
            f.write("\n".join(str(x) for x in append))

class TestInstalEvents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)

        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")
        cls.file_h.setLevel(LOGLEVEL)

        logging = logmod.root
        logging.setLevel(logmod.NOTSET)
        logging.addHandler(cls.file_h)


    @classmethod
    def tearDownClass(cls):
        logging.removeHandler(cls.file_h)

    def test_event_observation(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertNotIn("observed(null,0)", result)

    def test_event_observation_timestep(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEvent,1)", result)
        self.assertNotIn("observed(null,1)", result)

    def test_event_observation_twice(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent \nobserved basicExEvent at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)

        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("observed(basicExEvent,1)", result)


    def test_event_observation_null_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_inst.ial"], with_prelude=True)
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])
        solver.solve()

        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalInst)", result)
        self.assertIn("observed(null,0)", result)
        self.assertIn("observed(null,1)", result)
        self.assertIn("occurred(null,minimalInst,0)", result)
        self.assertIn("occurred(null,minimalInst,1)", result)
        self.assertIn("occurred(null,minimalInst,2)", result)
        # null events are generated:
        # self.assertIn("observed(null,0)", result)


    def test_event_observation_outside_time_bounds(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 10")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        solver.solve(query)

        self.assertEqual(len(solver.results), 1)
        result : str = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        # Event is not observed
        self.assertNotIn("observed(basicExEvent,10)", result)

    def test_event_observation_inside_extended_time_bounds(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 10")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=15'])

        solver.solve(query)

        self.assertEqual(len(solver.results), 1)
        result : str = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        # Event is not observed
        self.assertIn("observed(basicExEvent,10)", result)




    def test_event_observation_different_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent\nobserved secondEvent at 1")
        # Solve
        save_last(compiled)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)

        self.assertEqual(len(solver.results), 1)
        result : str = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("observed(secondEvent,1)", result)


    def test_event_observation_with_conflicting_times(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add events
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 0\nobserved secondEvent at 0")
        # Solve
        save_last(compiled)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        solver.solve(query)
        # There is not model for it:
        self.assertEqual(len(solver.results), 0)

    def test_event_observation_unrecognised(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed badEvent at 0")
        # Solve
        save_last(compiled)
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(_unrecognisedEvent,0)", result)

    def test_event_with_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithParam(first) at 0\nobserved basicExEventWithParam(second) at 1")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEventWithParam(first),0)", result)
        self.assertIn("observed(basicExEventWithParam(second),1)", result)
        self.assertNotIn("observed(null,0)", result)


    def test_event_with_unrecognized_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithVar(other) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertNotIn("observed(basicExEventWithParam(other),0)", result)

    def test_event_with_domain_extended_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEventWithParam(other) at 0")
        domain   = InstalDomainCompiler().compile(parser.parse_domain("Example : other"))
        # Solve
        solver   = ClingoSolver("\n".join(compiled + [domain]),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEventWithParam(other),0)", result)

    def test_event_with_multi_var(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_events.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEventMulti(first, second, third) at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        save_last(compiled, append=solver.results[0].atoms)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("institution(minimalEvents)", result)
        self.assertIn("observed(basicExEventMulti(first,second,third),0)", result)



##-- main
if __name__ == '__main__':
    unittest.main()

##-- end main
