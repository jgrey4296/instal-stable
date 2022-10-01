%% Translation of ${fluent} of ${source} xterminates ${response} of ${sink} if [condition]
xterminated(${source}, ${response}, ${sink}, I) :- instant(I),
                                                   bridge(${bridge}, ${source}, ${sink}),
                                                   holdsat(tpow(${source}, ${response}, ${sink}), ${bridge}, I),
                                                   holdsat(live(${bridge}), ${bridge}, I),
                                                   occurred(${fluent}, ${source}, I),
                                                   ${rhs}.
