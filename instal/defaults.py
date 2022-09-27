#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import os
##-- end imports

COMPILED_EXT = ".lp"

INST_EXT      = ".ial"
BRIDGE_EXT    = ".iab"
DOMAIN_EXT    = ".idc"

QUERY_EXT     = ".iaq"

# Equivalent:
FACT_EXT      = ".iaf"
SITUATION_EXT = ".iaf"

# Data:
DATA_loc             = "instal.__data"
STANDARD_PRELUDE_loc = "instal.__data.standard_prelude"
INSTITUTION_DATA_loc = "instal.__data.institution"
BRIDGE_DATA_loc      = "instal.__data.bridge"

TEX_loc              = "instal.__data.tex"

# Default groupings of holdsat in instal.interfaces.trace.State_i
STATE_HOLDSAT_GROUPS = ["perm", "pow", "tpow", "ipow", "gpow", "obl", "fluent", "other"]
