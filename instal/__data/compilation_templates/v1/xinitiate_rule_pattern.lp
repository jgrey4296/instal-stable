%% Translation of ${fluent} of ${source} xinitiates ${response} of ${sink} if [condition]
xinitiated(${source}, ${response}, ${sink}, I) :- instant(I),
                                                  bridge(${bridge}, ${source}, ${sink}),
                                                  holdsat(ipow(${source}, ${response}, ${sink}), ${bridge}, I),
                                                  holdsat(live(${bridge}), ${bridge}, I),
                                                  occurred(${fluent}, ${source}, I),
                                                  ${rhs}.
