#! /usr/bin/env python
"""
CLI program to load instal trace JSONs and select a subset,
for reporting

"""
##-- imports
from __future__ import annotations

import argparse
import json
import logging as logmod
import json
import os
import pathlib
from sys import stderr, stdout

from instal.report.gantt import InstalGanttReporter
from instal.report.pdf import InstalPDFReporter
from instal.report.text import InstalTextReporter
from instal.trace.trace import InstalTrace

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target',    help="Specify json file trace to load", required=True)
parser.add_argument("-o", "--output",    type=str, help="output dir location, defaults to {cwd}/instal_tmp")
parser.add_argument('-i', '--interactive', action="store_true")
parser.add_argument('-b', '--blacklist', action='append', help="regular expressions to reject terms by")
parser.add_argument('-w', '--whitelist', action='append', help="regular expressions to accept terms by")
parser.add_argument('-s', '--start',     default=0, type=int, help="The start of the range of timesteps to accept. Defaults to 0")
parser.add_argument('-e', '--end',       default=-1, type=int, help="The end of the range of timesteps to accept. Defaults to -1, meaning all")
parser.add_argument("-v", "--verbose",   action='count', help="turns on trace output, v for holdsat, vv for more")
parser.add_argument('--defs')
##-- end argparse


def main():
    ##-- Logging
    DISPLAY_LEVEL = logmod.WARNING
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

    logger          = logmod.root
    console_handler = logmod.StreamHandler(STREAM_TARGET)
    file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

    console_handler.setLevel(logmod.DEBUG)
    # console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
    file_handler.setLevel(logmod.DEBUG)
    # file_handler.setFormatter(logmod.Formatter(LOG_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logging = logger
    ##-- end Logging

    args       = parser.parse_args()
    assert(not (args.interactive and (args.blacklist or args.whitelist))), "Either use a black/whitelist or use interactive."

    if args.defs:
        args.defs = pl.Path(args.defs).expanduser().resolve()
        defaults.set_defaults(args.defs)


    # Set Logging level
    console_handler.setLevel(max(logmod.NOTSET, logmod.WARNING - (10 * self.verbose)))

    trace_path = pathlib.Path(args.target).expanduser().resolve()
    assert(trace_path.exists())
    assert(trace_path.suffix == ".json"), "You must specify a json trace to load"


    logging.info("Loading Trace: %s", trace_path)
    trace = InstalTrace.from_json(json.loads(trace_path.read_text()))

    if args.interactive:
        from instal.util.filter import filter_loop
        filter_loop(trace)
        exit()

    # Run a single filter
    filtered = trace.filter(args.whitelist or [], args.blacklist or [],
                            start=args.start, end=args.end)
    print("Filtered Trace: ")
    print(repr(filtered))

    if args.output:
        out_path      = pathlib.Path(args.output)
        as_json : str = filtered.to_json_str(out_path.name)

        with open(out_path, 'w') as f:
            f.write(trace_s)

##-- ifmain
if __name__ == "__main__":
    main()

##-- end ifmain
