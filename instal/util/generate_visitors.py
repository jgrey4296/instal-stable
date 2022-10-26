#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import argparse
import ast as pyAST
import pathlib
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from importlib.resources import files
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import instal.interfaces.ast as iAST

if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- data
data_file= files("instal.util").joinpath("base_visitor.py")
data_text = data_file.read_text()
##-- end data

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- argparse
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog = "\n".join([""]))
parser.add_argument('--target')
##-- end argparse

@dataclass
class ASTVisitGenerator(pyAST.NodeTransformer):

    asts : set[str] = field(default_factory=set)

    def visit_ClassDef(self, node):
        existing = {x.name for x in node.body}
        to_generate = {f"visit_{x}" for x in self.asts} - existing
        for func_name in sorted(to_generate):
            visit_method = pyAST.FunctionDef(func_name,
                                             args=pyAST.arguments(args=[pyAST.arg("self"),
                                                                        pyAST.arg("node")],
                                                                  posonlyargs=[],
                                                                  defaults=[],
                                                                  kwonlyargs=[]),
                                             body=[pyAST.parse("raise NotImplementedError()").body[0]],
                                             decorator_list=[],
                                             lineno=None)
            node.body.append(visit_method)

        return node

def main():
    args = parser.parse_args()

    # Load a partial class, or the stub
    if args.target is not None:
        args.target = pathlib.Path(args.target)
        with open(args.target, 'r') as f:
            base_module = pyAST.parse(f.read(), args.target)
    else:
        base_module = pyAST.parse(data_text)

    transformer = ASTVisitGenerator({x for x in dir(iAST)
                                     if "AST" in x and issubclass(getattr(iAST, x), iAST.InstalAST)})

    # Run the generator
    transformed_visitor = transformer.visit(base_module)

    # Turn back to source code
    gen_visitor = pyAST.unparse(transformed_visitor)

    # Print it, so it can be redirected to a file
    print(gen_visitor)

if __name__ == '__main__':
    main()
