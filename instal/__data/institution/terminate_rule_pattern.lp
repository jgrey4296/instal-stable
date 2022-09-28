%% Translation of ${event} terminates ${state} if [condition]
terminated(${state}, ${inst}, I) :- instant(I),
                                    institution(${inst}),
                                    inertialFluent(${state}, ${inst}),
                                    holdsat(live(${inst}), ${inst}, I),
                                    occurred(${event}, ${inst}, I),
                                    not occurred(violation(${event}), ${inst}, I),
                                    ${rhs}.
