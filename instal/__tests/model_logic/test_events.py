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
from instal.defaults import STANDARD_PRELUDE_loc
from instal.parser.parser import InstalPyParser
from instal.solve.clingo_solver import ClingoSolver

##-- end imports

##-- data
inst_prelude    = files(STANDARD_PRELUDE_loc)
test_files      = files("instal.__data.test_files.minimal")
##-- end data

##-- warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    pass
##-- end warnings
logging = logmod.root

def save_last(compiled):
    "A utility to save lines of text to a file for debugging compiled output "
    with open(pathlib.Path(__file__).parent / "last_run.lp", 'w') as f:
        f.write("\n".join(compiled))

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
        compiled = compile_target([test_files / "minimal_ex_event.ial"], with_prelude=True)
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
        self.assertIn("inst(minimalEx)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertNotIn("observed(null,0)", result)

    def test_event_observation_timestep(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_ex_event.ial"], with_prelude=True)
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
        self.assertIn("inst(minimalEx)", result)
        self.assertIn("observed(basicExEvent,1)", result)
        self.assertNotIn("observed(null,1)", result)

    def test_event_observation_twice(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_ex_event.ial"], with_prelude=True)
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
        self.assertIn("inst(minimalEx)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("observed(basicExEvent,1)", result)


    def test_event_observation_null_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_no_events.ial"], with_prelude=True)
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])
        solver.solve()

        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("inst(minimalNoEv)", result)
        self.assertIn("observed(null,0)", result)
        self.assertIn("observed(null,1)", result)
        self.assertIn("occurred(null,minimalNoEv,0)", result)
        self.assertIn("occurred(null,minimalNoEv,1)", result)
        self.assertIn("occurred(null,minimalNoEv,2)", result)
        # null events are generated:
        # self.assertIn("observed(null,0)", result)


    def test_event_observation_outside_time_bounds(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_ex_event.ial"], with_prelude=True)
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
        self.assertIn("inst(minimalEx)", result)
        # Event is not observed
        self.assertNotIn("observed(basicExEvent,10)", result)

    def test_event_observation_different_events(self):
        # Compile a harness
        compiled = compile_target([test_files / "two_ex_events.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed firstEvent \nobserved secondEvent at 1")
        # Solve
        save_last(compiled)
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)

        self.assertEqual(len(solver.results), 1)
        result : str = str(solver.results[0].shown)
        self.assertIn("inst(twoEvents)", result)
        self.assertIn("observed(firstEvent,0)", result)
        self.assertIn("observed(secondEvent,1)", result)


    def test_event_observation_with_conflicting_times(self):
        # Compile a harness
        compiled = compile_target([test_files / "two_ex_events.ial"], with_prelude=True)
        # Add events
        parser   = InstalPyParser()
        query    = parser.parse_query("observed firstEvent at 0\nobserved secondEvent at 0")
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
        compiled  = compile_target([test_files / "minimal_ex_event.ial"], with_prelude=True)
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
        self.assertIn("inst(minimalEx)", result)
        self.assertIn("observed(_unrecognisedEvent,0)", result)
    def test_event_recognition_unpermitted(self):
        # Compile a harness
        compiled = compile_target([test_files / "minimal_inst_event.ial"], with_prelude=True)
        # Add an event
        parser   = InstalPyParser()
        query    = parser.parse_query("observed basicExEvent at 0")
        # Solve
        solver   = ClingoSolver("\n".join(compiled),
                                options=['-n', "1",
                                         '-c', f'horizon=2'])

        # Check it is observed
        solver.solve(query)
        # solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)

        self.assertIn("inst(minimalInstEv)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("occurred(_unpermittedEvent(basicEvent_i),minimalInstEv,0)", result)

    def test_event_recognition_permitted(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_inst_event.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEvent at 0")
        situation = parser.parse_situation("initially perm(basicEvent_i) in minimalInstEv")
        # Solve
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("inst(minimalInstEv)", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("occurred(basicEvent_i,minimalInstEv,0)", result)




    def test_event_recognition_unempowered(self):
        # Compile a harness
        compiled  = compile_target([test_files / "minimal_inst_event_no_generate.ial"], with_prelude=True)
        # Add an event
        parser    = InstalPyParser()
        query     = parser.parse_query("observed basicExEvent at 0")
        situation = parser.parse_situation("initially perm(basicEvent_i) in minimalInstEv")
        # Solve
        save_last(compiled)
        solver    = ClingoSolver("\n".join(compiled),
                                 options=['-n', "1",
                                          '-c', f'horizon=2'])
        # Check it is observed
        solver.solve(query, situation)
        self.assertEqual(len(solver.results), 1)
        result = str(solver.results[0].shown)
        self.assertIn("inst(minimalInstEvNoGen", result)
        self.assertIn("observed(basicExEvent,0)", result)
        self.assertIn("occurred(null,minimalInstEvNoGen,0)", result)
        self.assertIn("occurred(_unempoweredEvent(basicExEvent),minimalInstEvNoGen,0)", result)
        self.assertNotIn("occurred(basicEvent_i", result)



##-- main
if __name__ == '__main__':
    unittest.main()

##-- end main
