#! /usr/bin/env python
"""
A Straightforward CLI Instal Compiler.
Give it a target file or directory,
and it will print the compiled logic program to stdout for redirection

Give it an output target, it'll write the logic program to that file.

Activate debugging to see the parser at work to identify parse problems.


"""
##-- imports
from __future__ import annotations

import argparse
import importlib
import logging as logmod
import pyparsing as pp
import pathlib
from importlib.resources import files
from io import StringIO
from sys import stderr, stdout
from typing import IO, List, Optional

from instal import defaults

from instal.interfaces.parser import InstalParser_i

##-- end imports

##-- Logging
logging = logmod.getLogger(__name__)
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target', help="Specify (multiple) files and directories to load", required=True)
argparser.add_argument('-o', '--output')
argparser.add_argument("-v", "--verbose", action='count', help="increase verbosity of logging (repeatable)")
argparser.add_argument('-d', '--debug', action="store_true")
argparser.add_argument('-c', '--check', action="store_true")
argparser.add_argument('-p', '--parser', default=defaults.PARSER, help="The import path for the parser class")
argparser.add_argument('--noprint', action="store_true")
argparser.add_argument('--defs')
##-- end argparse


def main():
    ##-- logging
    DISPLAY_LEVEL = logmod.DEBUG
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%% %(levelname)8s | %(message)s"
    FILE_FORMAT   = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

    logging = logmod.root
    logging.setLevel(logmod.NOTSET)
    console_handler = logmod.StreamHandler(STREAM_TARGET)
    file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

    console_handler.setLevel(DISPLAY_LEVEL)
    console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
    file_handler.setLevel(logmod.DEBUG)
    file_handler.setFormatter(logmod.Formatter(FILE_FORMAT))

    logging.addHandler(console_handler)
    logging.addHandler(file_handler)
    ##-- end logging

    args      = argparser.parse_args()

    if args.defs:
        args.defs = pl.Path(args.defs).expanduser().resolve()
        defaults.set_defaults(args.defs)

    # Set Logging Level
    console_handler.setLevel(max(logmod.NOTSET, logmod.WARNING - (10 * (args.verbose or 0))))

    args.target = pathlib.Path(args.target)
    if args.target.is_file():
        targets = [args.target]
    else:
        targets = list(args.target.iterdir())

    from instal.util.compilation import compile_target
    result = compile_target(targets, args.debug, with_prelude=True, check=args.check, parser_import=args.parser)

    if args.output:
        logging.info("Writing to Output: %s", args.output)
        with open(pathlib.Path(args.output), 'w') as f:
            f.write("\n".join(result))

    if not args.noprint:
        print("\n".join(result))
    else:
        logging.info("Not Printing Result")

##-- ifmain
if __name__ == '__main__':
    main()

##-- end ifmain
