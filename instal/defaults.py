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

# Parser import string:
PARSER = "instal.parser.v1.parser.InstalPyParser"

# Data:
COMP_DATA_loc        = "instal.__data.compilation_templates.v1"
STANDARD_PRELUDE_loc = "instal.__data.standard_prelude.v1"

TEX_loc              = "instal.__data.tex"

# Default groupings of holdsat in instal.interfaces.trace.State_i
STATE_HOLDSAT_GROUPS = ["perm", "pow", "tpow", "ipow", "gpow", "obl", "fluent", "other"]
