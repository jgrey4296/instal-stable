#! /usr/bin/env python
##-- imports
from __future__ import annotations

import argparse
import logging as logmod
import pathlib
from io import StringIO
from sys import stderr, stdout
from typing import IO, List, Optional

from clingo import Symbol, parse_term

from .models.InstalDummyModel import InstalDummyModel

##-- end imports

##-- Logging
DISPLAY_LEVEL = logmod.DEBUG
LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
FILE_MODE     = "w"
STREAM_TARGET = stderr # or stdout

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
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('--dir',               type=str, help="Specify a directory to load")
argparser.add_argument('-f', '--file',        action="append", help="Specify (multiple) specific files to load")
argparser.add_argument("-q", "--query",       type=str, help="specify query file (.iaq) - use \"-\" to take from stdin.")

argparser.add_argument("-o", "--output-file", type=str, help="output file/directory for one/several inputs: uses /tmp if omitted")
argparser.add_argument("-j", "--json-file",   type=str, help="specify json output file or directory")

argparser.add_argument("-v", "--verbose",     action='count', help="turns on trace output, v for holdsat, vv for more")
argparser.add_argument('-a', '--answer-set',  type=int, default=0, help='choose an answer set (default all)')
argparser.add_argument('-n', '--number',      type=int, default=1, help='compute at most <n> models (default 1, 0 for all)')
argparser.add_argument('-l', '--length',      type=int, default=0, help='length of trace (default 1)')
##-- end argparse


def instal_inspect():
    args = argparser.parse_args()

    file_group   = InstalFileGroup(args)
    option_group = InstalOptionGroup(verbose=args.verbose,
                                     answer_set=args.answer_set,
                                     length=args.length,
                                     number=args.number)

    model        = InstalDummyModel(filegroup, optgroup)
    declarations = model.get_declarations()
    logging.info("Inspection profile:")
    logging.info(declarations)



if __name__ == "__main__":
    instal_inspect()
