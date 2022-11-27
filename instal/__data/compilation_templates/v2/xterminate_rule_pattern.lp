%% Translation of ${fluent} of ${source} xterminates ${response} of ${sink} if [condition]
xTerminated(${source}, ${response}, ${sink}, I) :- instant(I),
                                                   bridge(${bridge}, ${source}, ${sink}),
                                                   holdsat(live(${bridge}), ${bridge}, I),
                                                   holdsat(deontic(termPower, ev(${source}, ${response}, ${sink})), ${bridge}, I),
                                                   occurred(${fluent}, ${source}, I),
                                                   ${rhs}.
