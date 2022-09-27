%%-- fluent rules
% All ifluents, nifluents are fluents:
fluent(F, I) :- ifluent(F, I).
fluent(F, I) :- nifluent(F, I).

% obligation fluents are inertial:
ifluent(F, I) :- ofluent(F, I).

% ifluent_change(fact, inst, time, type)
ifluent_change(P, In, I, initiated)		:- initiated(P, In, I), instant(I), inst(In).
ifluent_change(P, In, I, initiated)		:- xinitiated(InSo, P, In, I), inst(InSo), inst(In), instant(I).
ifluent_change(P, In, I, terminated)	:- terminated(P, In, I), instant(I), inst(In).
ifluent_change(P, In, I, terminated)	:- xterminated(InS, P, In, I), instant(I), inst(In), inst(InS).

% Translate external fluent setting to holding at the start of the trace
holdsat(F, I, J)						:- extHoldsat(F, I), start(J), ifluent(F, I).

% Propagate inertial fluents across timesteps:
holdsat(P, In, J)						:- ifluent_change(P, In, I, initiated), next(I, J), ifluent(P, In), instant(I), instant(J), inst(In).
holdsat(P, In, J)						:- holdsat(P, In, I), next(I, J), ifluent(P, In), instant(I), instant(J), inst(In), not ifluent_change(P, In, I, terminated).

%% TODO maybe replace pow/perm(Ev) with norm(Modality, Ev)
% All Institutions have norm fluents for all institution events
ifluent(perm(Ev), Ins) :- inst(Ins), eventType(Ev, Ins, inst).
ifluent(pow(Ev), Ins)  :- inst(Ins), eventType(Ev, Ins, inst).

% Null permissions hold from the start
holdsat(perm(null), Ins, I) :- start(I), inst(Ins).
holdsat(pow(null),  Ins, I) :- start(I), inst(Ins).

% Institutions also hold by default at the start:
% (which includes bridges, because they are institutions)
ifluent(live(Ins), Ins)    :- inst(Ins).
holdsat(live(Ins), Ins, I) :- start(I), inst(Ins).

% Reject all ifluent changes that aren't well formed:
:- ifluent_change(_, _, _, T), not ifluent_changes(T).
:- ifluent_change(F, _, _, _), not ifluent(F, _).

%%-- end fluent rules
