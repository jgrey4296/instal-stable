#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref
##-- end imports

logging = logmod.getLogger(__name__)

def main():
    print("Instal: An Institutional Action Language")
    print("CLI:")
    print("instalc: The Compiler")
    print("instalq: Run a Query")
    print("instalr: Generate a Trace Report")


if __name__ == "__main__":
    # TODO select options from instal.cli
    main()
