% initially: ${state} (if [conditions])
holdsat(${state}, ${inst}, I) :- inst(${inst}),
                                 start(I),
                                 not holdsat(live(${inst}), ${inst}),
                                 ${rhs}.
