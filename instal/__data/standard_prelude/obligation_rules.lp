%%-- obligation rules
% obligation completion are institutional events:
eventType(obligation(O), Ins, inst) :- obligationalFluent(obligation(O, _, _, _), Ins).
% As are violations:
eventType(violation(V), Ins, viol)  :- obligationalFluent(obligation(_, _, V, _), Ins).

% Initiation?

% An obligation terminates if it holds when it reaches its deadline
terminated(obligation(O, I, V, R), Ins, I) :- instant(I),
                                              institution(Ins),
                                              holdsat(obligation(O, I, V, R), Ins, I).

% An obligation terminates once its obligation is completed before its deadline
% *if* it is oneshot
terminated(obligation(O, D, V, oneshot), Ins, I) :- instant(I),
                                                    institution(Ins),
                                                    event(obligation(O)),
                                                    occurred(obligation(O), Ins, I),
                                                    holdsat(obligation(O, D, V, oneshot), Ins, I).

% or an obligation terminates if it is violated,
% *if* it is oneshot
terminated(obligation(O, D, V, oneshot), Ins, I) :- instant(I),
                                                    institution(Ins),
                                                    event(violation(V)),
                                                    occurred(violation(V), Ins, I),
                                                    holdsat(obligation(O, D, V, oneshot), Ins, I).

% reject all obligations that aren't well formed
:- obligationalFluent(obligation(_, _, _, R), _), not obligationTypes(R).

%%-- end obligation rules
