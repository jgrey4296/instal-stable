%% Translation of ${event} initiates ${state} if [condition]
initiated(${state}, ${inst}, I) :- instant(I),
                                   institution(${inst}),
                                   inertialFluent(${state}, ${inst}),
                                   holdsat(live(${inst}), ${inst}, I),
                                   occurred(${event}, ${inst}, I),
                                   not occurred(violation(${event}), ${inst}, I),
                                   ${rhs}.
