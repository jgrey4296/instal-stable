#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
import pathlib as pl
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


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

    from instal.compiler.bridge_compiler import InstalBridgeCompiler
    from instal.compiler.domain_compiler import InstalDomainCompiler
    from instal.compiler.institution_compiler import InstalInstitutionCompiler
    from instal.compiler.query_compiler import InstalQueryCompiler
    from instal.compiler.situation_compiler import InstalSituationCompiler


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
        compiler  = None
        parse_fn  = None
        validator = None

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
            ast = parse_fn(target)
            if check and validator:
                validator.validate(ast)

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
