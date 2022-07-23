%% Translation of {sf} of {sinst} xinitiates {x} of {dinst} if {condition}
%
xinitiated({sinst}, {x},{dinst},I) :-
    occurred({sf},{sinst},I),
    holdsat(ipow({sinst}, {x}, {dinst}), {inst}, I),
    holdsat(live({inst}),{inst},I),
    bridge({inst}),
    inst({dinst}),
    inst({sinst}),
