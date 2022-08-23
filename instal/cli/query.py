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
from instal.util.misc import InstalFileGroup, InstalOptionGroup

# from instal.model_runners.multi_shot import InstalMultiShotModel

from clingo import Control, Function, Symbol
##-- end imports

##-- Logging
if __name__ == '__main__':
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
else:
    logging = logmod.getLogger(__name__)
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target',      action="append", help="Specify (multiple) files and directories to load")

argparser.add_argument("-o", "--output",      type=str, help="output dir location, defaults to {cwd}/instal_tmp")
argparser.add_argument("-j", "--json",        action='store_true', help="toggle json output")

argparser.add_argument("-v", "--verbose",     action='count', help="turns on trace output, v for holdsat, vv for more")
argparser.add_argument('-a', '--answer-set',  type=int, default=0, help='choose an answer set (default all)')
argparser.add_argument('-n', '--number',      type=int, default=1, help='compute at most <n> models (default 1, 0 for all)')
argparser.add_argument('-l', '--length',      type=int, default=0, help='length of trace (default 1)')
argparser.add_argument('-d', '--debug',       action="store_true")
##-- end argparse
def main():
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
    compiled = compile_target(file_group.get_sources(), args.debug)

    logging.info("Starting Clingo")
    ctl = Control()

    for x in file_group.get_compiled():
        ctl.load(x)

    ctl.add("base", [], "\n".join(compiled))
    models = []

    def on_model_cb(model):
        models.append(InstalModelResult(model.symbols(atoms=True),
                                                model.symbols(shown=True),
                                                model.cost,
                                                model.number,
                                                model.optimality_proven,
                                                model.type))

        models.append(new_model)
        ## note: model destroyed on exit/reallocated in clingo

    logging.info("Grounding Program")
    ctl.ground([("base", [])])
    logging.info("Running Program")
    ctl.solve(on_model=on_model_cb)

    logging.info("Program Results:")
    for term in models[0].shown:
        logging.info(term)


if __name__ == "__main__":
    main()
