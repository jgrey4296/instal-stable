#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import argparse
import pathlib
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
import importlib
from uuid import UUID, uuid1
from weakref import ref
from instal import defaults

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
# If CLI:
# logging = logmod.root
# logging.setLevel(logmod.NOTSET)
##-- end logging

##-- argparse
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog = "\n".join([""]))
parser.add_argument('--parser', default="instal.parser.v1")
parser.add_argument('--out', required=True)
##-- end argparse


def main():
    global parser
    args     = parser.parse_args()
    args.out = pathlib.Path(args.out).expanduser().resolve()
    print("Test output:\n {},\n {}".format(args.out, args.parser))

    # Now import and build the parser
    parser_import     = args.parser + ".parse_funcs"
    parser_module     = importlib.import_module(parser_import)
    top_parsers =     [(x, getattr(parser_module, x)) for x in dir(parser_module)
                       if "top_" in x]
    for name, parser in top_parsers:
        print(f"Making Diagram for: {name}")
        parser.create_diagram(args.out / (name + "_railroad.html"),
                              3, True, True)



if __name__ == '__main__':
    main()
