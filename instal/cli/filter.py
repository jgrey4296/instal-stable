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
##-- end argparse

def filter_loop(trace):
    """ A Simple command loop to:
    print a trace,
    [w]hitelist terms from the trace (regex)
    [b]lacklist terms from the trace (regex]
    [r]ange the trace (int:int)
    [i]nfo about the trace
    [t]imestep (int)
    [s]ave it (path)
    [p]op from the stack of trace modifications
    [h]elp
    [q]uit
    """
    trace_stack  = [trace]
    last_command = ""
    while last_command != "q" and bool(trace_stack):
        current = trace_stack[-1]
        print(repr(current))
        print("----------")
        print("Trace Length       : ", len(current))
        print("Available Timesteps: ", ", ".join(str(x) for x in current.timesteps))
        last_command = input(f"[{len(trace_stack)}]: ")

        if last_command == "":
            continue

        if last_command == "qq":
            break

        try:
            match last_command[0]:
                case "q":
                    confirmed = input("Confirm Quit: Y/*? ")
                    if confirmed == "Y":
                        break
                    last_command = ""
                case "w":
                    trace_stack.append(current.filter(allow=[last_command[1:].strip()],
                                                      reject=[]))
                case "b":
                    trace_stack.append(current.filter(allow=[],
                                                      reject=[last_command[1:].strip()]))
                case "r":
                    the_range = [int(x) for x in last_command[1:].split(":")]
                    if last_command[1] == ":":
                        the_range.insert(0, 0)
                    if len(the_range) == 1:
                        the_range.append(-1)

                    if the_range[1] != -1 and the_range[1] < the_range[0]:
                        print("Range is Nonsensical: ", the_range)
                        input()
                        continue

                    trace_stack.append(current.filter(allow=[],
                                                      reject=[],
                                                      start=the_range[0],
                                                      end=the_range[1]))
                case "i":
                    print("Trace Length       : ", len(current))
                    print("Available Timesteps: ", ", ".join(str(x) for x in current.timesteps))
                    print("Institutions       : ", ", ".join(current.metadata['institutions']))
                    input()
                case "t":
                    step = int(last_command[1:])
                    try:
                        print(repr(current[step]))
                    except KeyError:
                        print("Timestep {} does not appear to be in this trace".format(step))
                        print("Available Timesteps: ")
                        print(", ".join(str(x) for x in current.timesteps))
                    input()
                case "s":
                    save_path     = pathlib.Path(last_command[1:].strip())
                    trace_s : str = current.to_json(save_path.name)
                    with open(save_path, 'w') as f:
                        f.write(trace_s)

                case "p":
                    print("Popping Trace")
                    trace_stack.pop()
                case "h":
                    print(filter_loop.__doc__)
                    input()
                case "d":
                    breakpoint()
                case _:
                    print("Unrecognized Filter Command: ", last_command)
        except Exception as err:
            print(err)
            input()


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

    # Set Logging level
    console_handler.setLevel(max(logmod.NOTSET, logmod.WARNING - (10 * self.verbose)))

    trace_path = pathlib.Path(args.target).expanduser().resolve()
    assert(trace_path.exists())
    assert(trace_path.suffix == ".json"), "You must specify a json trace to load"


    logging.info("Loading Trace: %s", trace_path)
    trace = InstalTrace.from_json(json.loads(trace_path.read_text()))

    if args.interactive:
        filter_loop(trace)
        exit()

    # Run a single filter
    filtered = trace.filter(args.whitelist or [], args.blacklist or [],
                            start=args.start, end=args.end)
    print("Filtered Trace: ")
    print(repr(filtered))

    if args.output:
        out_path      = pathlib.Path(args.output)
        as_json : str = filtered.to_json(out_path.name)

        with open(out_path, 'w') as f:
            f.write(trace_s)

if __name__ == "__main__":
    main()
