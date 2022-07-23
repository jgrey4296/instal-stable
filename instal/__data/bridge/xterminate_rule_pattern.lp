%% Translation of {sf} of {sinst} xterminates {x} of {dinst} if {condition}
xterminated({sinst}, {x},{dinst},I) :-
     occurred({sf},{sinst},I),
     holdsat(tpow({sinst}, {x}, {dinst}), {inst}, I),
     holdsat(live({inst}),{inst},I),
     bridge({inst}),
     inst({dinst}),
     inst({sinst}),
