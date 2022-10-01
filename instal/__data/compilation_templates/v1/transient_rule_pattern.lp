%% Translation of ${state} when ${rhs}
holdsat(${state}, ${inst}, I) :- instant(I),
                                 institution(${inst}),
                                 transientFluent(${state}, ${inst}),
                                 ${rhs}.
