% Institutional events
%
% Event: {ev} (type: in)
event({ev}{args})                    :- {rhs}.
evtype({ev}{args},{inst},inst)       :- {rhs}.
evinst({ev}{args},{inst})            :- {rhs}.
ifluent(perm({ev}{args}),{inst})     :- {rhs}.
fluent(perm({ev}{args}),{inst})      :- {rhs}.
event(viol({ev}{args}))              :- {rhs}.
evtype(viol({ev}{args}),{inst},viol) :- {rhs}.
evinst(viol({ev}{args}),{inst})      :- {rhs}.
