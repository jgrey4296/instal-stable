%% Translation of ${fluent} of ${source} xinitiates ${response} of ${sink} if [condition]
xInitiated(${source}, ${response}, ${sink}, I) :- instant(I),
                                                  bridge(${bridge}, ${source}, ${sink}),
                                                  holdsat(live(${bridge}), ${bridge}, I),
                                                  holdsat(deontic(initPow, ev(${source}, ${response}, ${sink})), ${bridge}, I),
                                                  occurred(${fluent}, ${source}, I),
                                                  ${rhs}.
