% TODO replace ipow with {powtype}
ifluent(ipow({sinst},{f},{dinst}), {inst}) :-
    inst({sinst}),
    source({sinst}, {inst}),
    inst({dinst}),
    sink({dinst}, {inst}),
    bridge({inst}),

