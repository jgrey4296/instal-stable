#! /usr/bin/env python
"""
CLI program to Compile and Run an Instal logic program.

If you point it to a compiled logic program, it will run that without parsing it.

Can Supplement the logic program with initial situational facts, and a query.

Prints result traces to the output directory, as strings, or json.
"""
##-- imports
from __future__ import annotations

import argparse
import logging as logmod
import pathlib
from importlib.resources import files
from io import StringIO
from sys import stderr, stdout
from typing import IO, List, Optional

from clingo import Control, Function, Symbol, parse_term
from instal.solve.clingo_solver import ClingoSolver
from instal.util.misc import InstalFileGroup, InstalOptionGroup
from instal.trace.trace import InstalTrace
from instal.defaults import STANDARD_PRELUDE_loc
##-- end imports

##-- Logging
logging = logmod.getLogger(__name__)
logging.setLevel(logmod.DEBUG)
##-- end Logging

##-- data
inst_prelude    = files(STANDARD_PRELUDE_loc)
##-- end data

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target',      action="append", help="Specify (multiple) files and directories to load")
argparser.add_argument('-s', '--situation',   help="Specify a string or file to parse of initial specs")
argparser.add_argument('-q', '--query',       help="Specify a string or file to parse of observed events")

argparser.add_argument("-o", "--output",      type=str, help="output dir location, defaults to {cwd}/instal_tmp")
argparser.add_argument("-j", "--json",        action='store_true', help="toggle json output")

argparser.add_argument("-v", "--verbose",     action='count', help="increase verbosity of logging (repeatable)")
argparser.add_argument('-a', '--answer-set',  type=int, default=0, help='choose an answer set (default all)')
argparser.add_argument('-n', '--number',      type=int, default=1, help='compute at most <n> models (default 1, 0 for all)')
argparser.add_argument('-l', '--length',      type=int, default=3, help='length of model trace (default 3)')
argparser.add_argument('-d', '--debug',       action="store_true", help="activate debug parser functions")
##-- end argparse

def maybe_get_query_and_situation(que:None|str, sit:None|str) -> tuple[list[TermAST], list[TermAST]]:
    """
    Try to parse a query and situation specification,
    without erroring if no targets are provided

    Returns a tuple of lists of TermASTs, which are empty if the targets produce nothing
    """
    from instal.parser.parser import InstalPyParser
    parser    = InstalPyParser()
    situation = []
    query     = []

    if sit:
        try:
            sit_path = pathlib.Path(sit).expanduser().resolve()
            assert(sit_path.exists())
            sit_text = sit_path.read_text()
        except:
            sit_text = sit.replace("\\n", "\n")

        situation += parser.parse_situation(sit_text).body[:]


    if que:
        try:
            query_path = pathlib.Path(que).expanduser().resolve()
            assert(query_path.exists())
            query_text = query_path.read_text()
        except:
            query_text = que.replace("\\n", "\n")

        query += parser.parse_query(query_text).body[:]


    return query, situation

def main():
    ##-- Logging
    DISPLAY_LEVEL = logmod.DEBUG
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

    logmod.root.setLevel(DISPLAY_LEVEL)
    logger          = logmod.getLogger(__name__)
    console_handler = logmod.StreamHandler(STREAM_TARGET)
    file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

    console_handler.setLevel(DISPLAY_LEVEL)
    # console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
    file_handler.setLevel(logmod.DEBUG)
    # file_handler.setFormatter(logmod.Formatter(LOG_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logging = logger
    logging.setLevel(logmod.DEBUG)
    ##-- end Logging

    args         = argparser.parse_args()
    file_group   = InstalFileGroup.from_targets(*args.target)
    option_group = InstalOptionGroup(verbose=args.verbose if args.verbose else 0,
                                     answer_set=args.answer_set,
                                     length=args.length,
                                     number=args.number,
                                     output=pathlib.Path(args.output) if args.output else None,
                                     json=args.json)

    logging.info("Starting Compile -> Query")
    from instal.cli.compiler import compile_target
    compiled         = compile_target(file_group.get_sources(), args.debug)
    prelude_files    = list(inst_prelude.iterdir())
    query, situation = maybe_get_query_and_situation(args.query, args.situation)

    solver        = ClingoSolver("\n".join(compiled),
                                 input_files=prelude_files + file_group.get_compiled(),
                                 options=['-n', str(option_group.number),
                                          '-c', f'horizon={option_group.length}'])

    num_models = solver.solve(query)

    if num_models == 0:
        logging.info("Found No Models")
        exit()

    logging.info("Program Results:")
    traces = []
    for i, result in enumerate(solver.results):
        logging.debug("Result %s:", i)
        logging.debug(" ".join(str(x) for x in result.shown))
        # Convert to a Trace of States.
        trace = InstalTrace.from_model(result,
                                       steps=option_group.length,
                                       metadata=solver.metadata.copy())
        traces.append(trace)

    breakpoint()

    match args.output, args.json:
        case None, _:
            pass
        case str(), False:
            # print out as text to output
            for trace in traces:
                trace_s : str = str(trace)
                # write out the basic representation
                pass
        case str(), True:
            # print out as json to output
            for trace in traces:
                trace_j : str = trace.to_json()
                # write out the json
                pass


if __name__ == "__main__":
    main()
