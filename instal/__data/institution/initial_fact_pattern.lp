% initially: ${state} (if [conditions])
holdsat(${state}, ${inst}, I) :- inst(${inst}),
                                 ifluent(${state}),
                                 start(I),
                                 holdsat(live(${inst}), I),
                                 ${rhs}.
