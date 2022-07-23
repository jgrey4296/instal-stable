%% Exogenous events

% Event: {ev} (type: ex)
event({ev}{args}) :- {rhs}.
evtype({ev}{args},{inst},ex) :- {rhs}.
evinst({ev}{args},{inst}) :- {rhs}.
ifluent(pow({ev}{args}),{inst}) :- {rhs}.
ifluent(perm({ev}{args}),{inst}) :- {rhs}.
fluent(pow({ev}{args}),{inst}) :- {rhs}.
fluent(perm({ev}{args}),{inst}) :- {rhs}.
event(viol({ev}{args})) :- {rhs}.
evtype(viol({ev}{args}), {inst}, viol) :- {rhs}.
evinst(viol({ev}{args}),{inst}) :- {rhs}.
