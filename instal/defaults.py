#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import os
import pathlib as pl
from importlib.resources import files
import tomlguard as TG

##-- end imports

default_toml  = files("instal.__data") / "defaults.toml"

data = TG.load(default_toml.read_text())
__loaded_toml = data.tool.instal

def __getattr__(attr):
    result = __loaded_toml.get(attr)
    if result is None:
        raise TG.TomlAccessError(attr)

    if isinstance(result, dict):
        return TG.TomlAccessor(attr, result)

    return result


def __dir__():
    return list(__loaded_toml.keys())

def set_defaults(path: pl.Path):
    global __loaded_toml
    __loaded_toml = TG.load(path.read_text()).tool.instal
