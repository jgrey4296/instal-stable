#!/bin/bash
# ../../instalsolve.py $@ \
../../instalremote.py $@ \
-i InstALFiles/libB.ial InstALFiles/pubA.ial InstALFiles/libC.ial \
-d DomainFiles/domain.idc \
-f InstALFiles/library.iaf \
-q TestTrace/coord-events.iaq \
-j coord-remote.json

