#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import os
##-- end imports

COMPILED_EXT = ".lp"

INST_EXT     = ".ial"
BRIDGE_EXT   = ".iab"
FACT_EXT     = ".iaf"
DOMAIN_EXT   = ".idc"
QUERY_EXT    = ".iaq"

INSTAL_API = os.environ.get("INSTAL_REMOTE_URL", "http://127.0.0.1:5000")
