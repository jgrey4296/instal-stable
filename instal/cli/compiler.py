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
from instal.compiler.bridge_compiler import InstalBridgeCompiler
from instal.compiler.domain_compiler import InstalDomainCompiler
from instal.compiler.institution_compiler import InstalInstitutionCompiler
from instal.compiler.query_compiler import InstalQueryCompiler
from instal.compiler.situation_compiler import InstalSituationCompiler

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

##-- end argparse

def compile_target(targets:list[pathlib.Path], debug=False, with_prelude=False, check=False, parser_import:str=defaults.PARSER) -> list[str]:
    """
    Compile targets (an explicit list, will not search or handle directories)
    using the default pyparsing parser.
    debug=True will activate parsing debug functions before loading the parser.

    with_prelude=True includes the default instal prelude from insta.__data.standard_prelude
    in the output.

    Returns a list of strings of each separate compiled file addition.
    """
    logging.info("Compiling %s target files", len(targets))

    if debug:
        logging.warning("Activating Parser Debug Functions")
        # Load pyparsing debug functions *before* loading a parser,
        # so all constructed objects have the functions set.
        import instal.parser.debug_functions as dbf
        dbf.debug_pyparsing()

    # Now import and build the parser
    parser_module_str = ".".join(parser_import.split(".")[:-1])
    parser_class_str  = parser_import.split(".")[-1]
    logging.info("Loading Parser Module : %s", parser_module_str)
    parser_module     = importlib.import_module(parser_module_str)
    logging.info("Loading Parser Class  : %s", parser_class_str)
    parser            = getattr(parser_module, parser_class_str)()

    assert(isinstance(parser, InstalParser_i))

    output : list[str] = []
    prelude_classes    = set()

    # Read each target, matching its suffix to choose
    # how to parse, check, and compile it
    compilation_errored = False
    for target in targets:
        logging.info("Reading %s", str(target))
        compiler = None
        parse_fn = None
        checker  = None
        text = target.read_text()

        ##-- match
        match target.suffix:
            case defaults.INST_EXT:
                parse_fn = parser.parse_institution
                compiler = InstalInstitutionCompiler()
            case defaults.BRIDGE_EXT:
                parse_fn = parser.parse_bridge
                compiler = InstalBridgeCompiler()
            case defaults.QUERY_EXT:
                parse_fn = parser.parse_query
                compiler = InstalQueryCompiler()
            case defaults.DOMAIN_EXT:
                parse_fn = parser.parse_domain
                compiler = InstalDomainCompiler()
            case defaults.SITUATION_EXT:
                parse_fn = parser.parse_situation
                compiler = InstalSituationCompiler()
            case _:
                logging.warning("Unrecognized compilation target: %s", target)
                continue


        ##-- end match

        # guard against repeated addition of preludes
        if with_prelude and compiler.__class__ not in prelude_classes:
            prelude_classes.add(compiler.__class__)
            output.append(compiler.load_prelude())

        try:
            ast = parse_fn(text, parse_source=target)
            if check and checker:
                checker.check(ast)

            compiled     = compiler.compile(ast)
            output.append(compiled)
        except pp.ParseException as exp:
            compilation_errored = True
            logging.error(f"File: %s : (line %s column %s) : %s : %s",
                            target.name, exp.lineno, exp.col, exp.msg, exp.markInputline())
        except pp.ParseFatalException as exp:
            compilation_errored = True
            logging.error(f"File: %s : (line %s column %s) : %s : %s",
                            target.name, exp.lineno, exp.col, exp.msg, exp.markInputline())
        except AssertionError as err:
            compilation_errored = True
            logging.error("File: %s : %s", target.name, str(err))
        except Exception as err:
            compilation_errored = True
            logging.error("File: %s : %s", target.name, str(err))


    if compilation_errored:
        logging.error("Compilation Errored Out")
        return []

    logging.info("Parse and Compilation Finished")
    return output

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

    # Set Logging Level
    console_handler.setLevel(max(logmod.NOTSET, logmod.WARNING - (10 * (args.verbose or 0))))

    args.target = pathlib.Path(args.target)
    if args.target.is_file():
        targets = [args.target]
    else:
        targets = list(args.target.iterdir())

    result = compile_target(targets, args.debug, with_prelude=True, check=args.check, parser_import=args.parser)

    if args.output:
        logging.info("Writing to Output: %s", args.output)
        with open(pathlib.Path(args.output), 'w') as f:
            f.write("\n".join(result))

    if not args.noprint:
        print("\n".join(result))
    else:
        logging.info("Not Printing Result")

if __name__ == '__main__':
    main()
