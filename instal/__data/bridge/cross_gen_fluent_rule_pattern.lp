fluent(gpow({sinst},{e},{dinst}), {inst}) :-
    inst({sinst}),
    source({sinst}, {inst}),
    inst({dinst}),
    sink({dinst}, {inst}),
    bridge({inst}),
    event({e}),
    evinst({e}, {dinst}),
    evtype({e}, {dinst}, ex),
    {te}.
