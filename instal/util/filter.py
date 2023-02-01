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

def filter_loop(trace):
    """ A Simple command loop to:
    print a trace,
    [w]hitelist terms from the trace (regex)
    [b]lacklist terms from the trace (regex]
    [r]ange the trace (int:int)
    [i]nfo about the trace
    [t]imestep (int)
    [s]ave it (path)
    [p]op from the stack of trace modifications
    [h]elp
    [q]uit
    """
    trace_stack  = [trace]
    last_command = ""
    while last_command != "q" and bool(trace_stack):
        current = trace_stack[-1]
        print(repr(current))
        print("----------")
        print("Trace Length       : ", len(current))
        print("Available Timesteps: ", ", ".join(str(x) for x in current.timesteps))
        last_command = input(f"[{len(trace_stack)}]: ")

        if last_command == "":
            continue

        if last_command == "qq":
            break

        try:
            match last_command[0]:
                case "q":
                    confirmed = input("Confirm Quit: Y/*? ")
                    if confirmed == "Y":
                        break
                    last_command = ""
                case "w":
                    trace_stack.append(current.filter(allow=[last_command[1:].strip()],
                                                      reject=[]))
                case "b":
                    trace_stack.append(current.filter(allow=[],
                                                      reject=[last_command[1:].strip()]))
                case "r":
                    the_range = [int(x) for x in last_command[1:].split(":")]
                    if last_command[1] == ":":
                        the_range.insert(0, 0)
                    if len(the_range) == 1:
                        the_range.append(-1)

                    if the_range[1] != -1 and the_range[1] < the_range[0]:
                        print("Range is Nonsensical: ", the_range)
                        input()
                        continue

                    trace_stack.append(current.filter(allow=[],
                                                      reject=[],
                                                      start=the_range[0],
                                                      end=the_range[1]))
                case "i":
                    print("Trace Length       : ", len(current))
                    print("Available Timesteps: ", ", ".join(str(x) for x in current.timesteps))
                    print("Institutions       : ", ", ".join(current.metadata['institutions']))
                    input()
                case "t":
                    step = int(last_command[1:])
                    try:
                        print(repr(current[step]))
                    except KeyError:
                        print("Timestep {} does not appear to be in this trace".format(step))
                        print("Available Timesteps: ")
                        print(", ".join(str(x) for x in current.timesteps))
                    input()
                case "s":
                    save_path     = pathlib.Path(last_command[1:].strip())
                    trace_s : str = current.to_json_str(save_path.name)
                    with open(save_path, 'w') as f:
                        f.write(trace_s)

                case "p":
                    print("Popping Trace")
                    trace_stack.pop()
                case "h":
                    print(filter_loop.__doc__)
                    input()
                case "d":
                    breakpoint()
                case _:
                    print("Unrecognized Filter Command: ", last_command)
        except Exception as err:
            print(err)
            input()
