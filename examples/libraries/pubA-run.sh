#!/bin/bash
~/Projects/instal-stable/instalsolve.py $@ \
-i InstALFiles/pubA.ial \
-q TestTrace/pubA-events.iaq \
-d DomainFiles/domain.idc \
-j pubA.json
