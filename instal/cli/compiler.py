#! /usr/bin/env python
##-- imports
from __future__ import annotations

import argparse
import logging as logmod
import pathlib
from importlib.resources import files
from io import StringIO
from sys import stderr, stdout
from typing import IO, List, Optional

from instal import defaults
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.compiler.bridge_compiler import InstalBridgeCompiler
from instal.compiler.query_compiler import InstalQueryCompiler
from instal.compiler.situation_compiler import InstalSituationCompiler
##-- end imports

##-- Logging
if __name__ == '__main__':
    DISPLAY_LEVEL = logmod.DEBUG
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

    logger          = logmod.root
    logger.setLevel(logmod.DEBUG)
    console_handler = logmod.StreamHandler(STREAM_TARGET)
    file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

    console_handler.setLevel(DISPLAY_LEVEL)
    # console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
    file_handler.setLevel(logmod.DEBUG)
    # file_handler.setFormatter(logmod.Formatter(LOG_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logging = logger
else:
    logging = logmod.getLogger(__name__)
    logging.setLevel(logmod.DEBUG)
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target', help="Specify (multiple) files and directories to load")
argparser.add_argument('-d', '--debug', action="store_true")
argparser.add_argument('-o', '--output')
##-- end argparse

##-- data
inst_prelude    = files("instal.__data.standard_prelude")

##-- end data

def load_prelude() -> str:
    assert(inst_prelude.is_dir())
    text = []
    for path in inst_prelude.iterdir():
        text += path.read_text().split("\n")

    return "\n".join(text)

def compile_target(targets:list[pathlib.Path], debug=False):
    logging.info("%% Compiling %s target files", len(targets))
    if debug:
        import instal.parser.debug_functions as dbf
        dbf.debug_pyparsing()

    import instal.parser.pyparse_institution as pi
    parser   = pi.InstalPyParser()

    output : list[str] = []

    for target in targets:
        logging.info("%% Reading %s", str(target))
        # read the target
        text = target.read_text()
        match target.suffix:
            case defaults.INST_EXT:
                ast          = parser.parse_institution(text)
                compiler     = InstalInstitutionCompiler()
                compiled     = compiler.compile(ast)
                prelude_text = load_prelude()
                output.append(prelude_text)
                output.append(compiled)
            case defaults.BRIDGE_EXT:
                ast          = parser.parse_bridge(text)
                compiler     = InstalBridgeCompiler()
                compiled     = compiler.compile(ast)
                output.append(compiled)
            case defaults.QUERY_EXT:
                ast          = parser.parse_query(text)
                compiler     = InstalQueryCompiler()
                compiled     = compiler.compile(ast)
                output.append(compiled)
            case defaults.DOMAIN_EXT:
                ast      = parser.parse_domain(text)
                compiler = InstalDomainCompiler()
                compiled = compiler.compile(ast)
                output.append(compiled)
            case defaults.SITUATION_EXT:
                ast          = parser.parse_situation(text)
                compiler     = InstalSituationCompiler()
                compiled     = compiler.compile(ast)
                output.append(compiled)
            case _:
                logging.warning("Unrecognized compilation target: %s", target)

    return output

def main():
    args        = argparser.parse_args()
    args.target = pathlib.Path(args.target)
    if args.target.is_file():
        targets = [args.target]
    else:
        targets = list(args.target.iterdir())

    result = compile_target(targets, args.debug)

    if args.output:
        with open(pathlib.Path(args.output), 'w') as f:
            f.write("\n".join(result))


    print("\n".join(result))


if __name__ == "__main__":
    main()
