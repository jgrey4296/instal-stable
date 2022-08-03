%% Translation of ${fluent} of ${source} xterminates ${response} of ${sink} if ${condition}
xterminated(${source}, ${response},${sink},I) :-
     occurred(${fluent},${source},I),
     holdsat(tpow(${source}, ${response}, ${sink}), ${bridge}, I),
     holdsat(live(${bridge}),${bridge},I),
     bridge(${bridge}, ${source}, ${sink}),
     instant(I),
     ${rhs}.
