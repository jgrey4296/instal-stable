% TODO replace ipow with {pow_type}
fluent(ipow({sinst},{f},{dinst}), {inst}) :-
    inst({sinst}),
    source({sinst}, {inst}),
    inst({dinst}),
    sink({dinst}, {inst}),
    bridge({inst}),
