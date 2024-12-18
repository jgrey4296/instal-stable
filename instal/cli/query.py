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
from json import dumps

from clingo import Control, Function, Symbol, parse_term
from instal.solve.clingo_solver import ClingoSolver
from instal.trace.trace import InstalTrace
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)

##-- end logging

##-- data
##-- end data

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target',      action="append", help="Specify (multiple) files and directories to load", required=True)
argparser.add_argument('-s', '--situation',   help="Specify a string or file to parse of initial specs")
argparser.add_argument('-q', '--query',       help="Specify a string or file to parse of observed events")

argparser.add_argument("-o", "--output",      type=str, help="output dir location, defaults to {cwd}/instal_tmp")
argparser.add_argument("-j", "--json",        action='store_true', help="toggle json output")

argparser.add_argument("-v", "--verbose",     action='count', help="increase verbosity of logging (repeatable)")
argparser.add_argument('--logfilter',         action="append", default=[])
argparser.add_argument('-a', '--answer-set',  type=int, default=0, help='choose an answer set (default all)')
argparser.add_argument('-n', '--number',      type=int, default=1, help='compute at most <n> models (default 1, 0 for all)')
argparser.add_argument('-l', '--length',      type=int, default=3, help='length of model trace (default 3)')
argparser.add_argument('-d', '--debug',       action="store_true", help="activate debug parser functions")
##-- end argparse

def main():
    ##-- logging
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%(levelname)8s | %(name)8s | %(message)s"
    FILE_FORMAT   = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

    logging = logmod.root
    logging.setLevel(logmod.NOTSET)
    console_handler = logmod.StreamHandler(STREAM_TARGET)
    file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

    console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
    file_handler.setLevel(logmod.DEBUG)
    file_handler.setFormatter(logmod.Formatter(FILE_FORMAT))

    logging.addHandler(console_handler)
    logging.addHandler(file_handler)
    ##-- end logging

    args         = argparser.parse_args()

    # Set Logging level
    console_handler.setLevel(max(logmod.NOTSET, logmod.WARNING - (10 * self.verbose)))

    args.output = pathlib.Path(args.output if args.output else "instal_tmp").expanduser().resolve()

    for name in args.logfilter:
        console_handler.addFilter(logmod.Filter(name))

    logging.info("Starting Compile -> Query")
    from instal.util.compilation import compile_target
    from instal.util.misc import maybe_get_query_and_situation
    from instal.defaults import STANDARD_PRELUDE_loc
    inst_prelude    = files(STANDARD_PRELUDE_loc)
    compiled         = compile_target(file_group.get_sources(), args.debug)
    prelude_files    = list(inst_prelude.iterdir())
    query, situation = maybe_get_query_and_situation(args.query, args.situation)

    solver           = ClingoSolver("\n".join(compiled),
                                    input_files=prelude_files + file_group.get_compiled(),
                                    options=['-n', str(args.number),
                                             '-c', f'horizon={args.length}'])
    num_models       = solver.solve(query)

    if num_models == 0:
        logging.info("Found No Models")
        exit()

    print("Program Results:")
    traces = []
    for i, result in enumerate(solver.results):
        print(f"Result {i}:")
        print(" ".join(str(x) for x in result.shown))
        print("")
        # Convert to a Trace of States.
        trace = InstalTrace.from_model(result,
                                       steps=args.length,
                                       metadata=solver.metadata.copy(),
                                       sources=file_group.get_sources())
        traces.append(trace)

    ext : str = ".json" if args.json else ".txt"
    logging.info("Writing Traces to %s/trace_[num]%s", args.output, ext)
    for i, trace in enumerate(traces):
        trace_s : str = ""
        current_filename = f"trace_{i}{ext}"
        match args.json:
            case False:
                trace_s = repr(trace)
            case True:
                trace_s = trace.to_json_str(current_filename)

        with open(args.output / current_filename, 'w') as f:
            f.write(trace_s)

##-- ifmain
if __name__ == "__main__":
    main()

##-- end ifmain
