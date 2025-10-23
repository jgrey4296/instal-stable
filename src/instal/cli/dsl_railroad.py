#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import argparse
import importlib
import logging as logmod
import pathlib
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from sys import stderr, stdout
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import pyparsing as pp
from instal import defaults

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- Logging
DISPLAY_LEVEL = logmod.WARN
LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
FILE_MODE     = "w"
STREAM_TARGET = stdout

logging         = logmod.root
logging.setLevel(logmod.NOTSET)
console_handler = logmod.StreamHandler(STREAM_TARGET)
file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

console_handler.setLevel(DISPLAY_LEVEL)
# console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
file_handler.setLevel(logmod.DEBUG)
# file_handler.setFormatter(logmod.Formatter(LOG_FORMAT))

logger.addHandler(console_handler)
logger.addHandler(file_handler)
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog = "\n".join([""]))
argparser.add_argument('--parser', default="instal.parser.v1", help="The import path to the parser package")
argparser.add_argument('--out', required=True)
argparser.add_argument('--defs')
##-- end argparse

def main():

    args     = argparser.parse_args()
    args.out = pathlib.Path(args.out).expanduser().resolve()
    print("Outputting diagrams to: %s", args.out)

    if args.defs:
        args.defs = pl.Path(args.defs).expanduser().resolve()
        defaults.set_defaults(args.defs)

    # Now import and build the argparser
    parser_import = args.parser + ".parse_funcs"
    print(f"Importing {parser_import}")

    parser_module = importlib.import_module(parser_import)
    top_parsers   = [(x, getattr(parser_module, x)) for x in dir(parser_module) if "top_" in x]
    for name, parser in top_parsers:
        print(f"Making Diagram for: {name}")
        parser.create_diagram(args.out / (name + "_railroad.html"),
                              3, True, True)



if __name__ == '__main__':
    main()
