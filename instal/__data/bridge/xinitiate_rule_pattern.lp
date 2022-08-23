%% Translation of ${fluent} of ${source} xinitiates ${response} of ${sink} if [condition]
xinitiated(${source}, ${response}, ${sink}, I) :-
    occurred(${fluent}, ${source}, I),
    holdsat(ipow(${source}, ${response}, ${sink}), ${bridge}, I),
    holdsat(live(${bridge}), ${bridge}, I),
    bridge(${bridge}, ${source}, ${sink}),
    instant(I),
    ${rhs}.
