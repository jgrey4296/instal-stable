% initially: ${state} (if [conditions])
holdsat(${state}, ${inst}, I) :- start(I),
                                 institution(${inst}),
                                 inertialFluent(${state}, ${inst}),
                                 holdsat(live(${inst}), ${inst}, I),
                                 ${rhs}.
