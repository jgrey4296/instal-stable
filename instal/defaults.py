#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import os
##-- end imports

##-- file extensions
COMPILED_EXT = ".lp"

INST_EXT      = ".ial"
BRIDGE_EXT    = ".iab"
DOMAIN_EXT    = ".idc"

QUERY_EXT     = ".iaq"

# Equivalent:
FACT_EXT      = ".iaf"
SITUATION_EXT = ".iaf"

##-- end file extensions

##-- parser selection
# Parser import string:
PARSER = "instal.parser.v2.parser.InstalPyParser"

##-- end parser selection

##-- data locations
# Data:
COMP_DATA_loc        = "instal.__data.compilation_templates.v2"
STANDARD_PRELUDE_loc = "instal.__data.standard_prelude.v2"

TEX_loc              = "instal.__data.tex"

##-- end data locations

##-- trace fluent groupings
# Default groupings of holdsat in instal.interfaces.trace.State_i
STATE_HOLDSAT_GROUPS = ["fluent", "gpow", "ipow", "obl", "other", "perm", "pow", "tpow"]

##-- end trace fluent groupings

DEONTICS = ["pow", "perm", "obl", "gpow", "ipow", "tpow"]


# DEBUG controls:
SUPPRESS_PARSER_EXCEPTION_TRACE = True
