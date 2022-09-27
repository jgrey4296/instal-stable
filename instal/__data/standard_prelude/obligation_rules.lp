%%-- obligation rules
% obligation completion are institutional events:
eventType(obl(O), Ins, inst) :- ofluent(obl(O, _, _, _), Ins).
% As are violations:
eventType(viol(V), Ins, viol) :- ofluent(obl(_, _, V, _), Ins).

% Initiation?

% An obligation terminates if it holds when it reaches its deadline
terminated(obl(O, I, V, R), Ins, I) :- inst(Ins), instant(I), holdsat(obl(O, I, V, R), Ins, I).

% An obligation terminates once its obligation is completed before its deadline
% *if* it is oneshot
terminated(obl(O, D, V, oneshot), Ins, I) :- instant(I), inst(Ins), event(obl(O)),  occurred(obl(O), Ins, I), holdsat(obl(O, D, V, oneshot), Ins, I).

% or an obligation terminates if it is violated,
% *if* it is oneshot
terminated(obl(O, D, V, oneshot), Ins, I) :- instant(I), inst(Ins), event(viol(V)), occurred(viol(V), Ins, I), holdsat(obl(O, D, V, oneshot), Ins, I).

% reject all obligations that aren't well formed
:- ofluent(obl(_, _, _, R), _), not obligation_types(R).


%%-- end obligation rules
