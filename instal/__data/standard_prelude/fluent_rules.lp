%%-- fluent rules
% All inertial and transient fluents are fluents
fluent(F, I) :- inertialfluent(F, I).
fluent(F, I) :- transientFluent(F, I).

% obligational fluents are inertial:
transientFluent(F, I) :- obligationalFluent(F, I).

% inertialFluentChange(fact, inst, time, type)
inertialFluentChange(P, In, I, initiated)    :- instant(I),
                                                institution(In),
                                                inertialFluent(P, In),
                                                initiated(P, In, I).

inertialFluentChange(P, Sink, I, initiated)  :- instant(I),
                                                institution(Source),
                                                institution(Sink).
                                                inertialFluent(P, Sink),
                                                xInitiated(Source, P, Sink, I).

inertialFluentChange(P, In, I, terminated)   :- instant(I),
                                                institution(In),
                                                inertialFluent(P, In),
                                                terminated(P, In, I).

inertialFluentChange(P, Sink, I, terminated) :- instant(I),
                                                institution(Source),
                                                institution(Sink),
                                                inertialFluent(P, Sink),
                                                xTerminated(Source, P, Sink, I).

% Translate external fluent setting to holding at the start of the trace
holdsat(F, I, J)						:- extHoldsat(F, I), start(J), inertialFluent(F, I).

% Propagate inertial fluents across timesteps:
holdsat(P, In, J)						:- next(I, J),
                               institution(In),
                               inertialFluent(P, In),
                               inertialFluentChange(P, In, I, initiated).

holdsat(P, In, J)						:- next(I, J),
                               institution(In),
                               inertialFluent(P, In),
                               holdsat(P, In, I),
                               not inertialFluentChange(P, In, I, terminated).

%% TODO maybe replace pow/perm(Ev) with norm(Modality, Ev)
% All Institutions have norm fluents for all institution events
inertialFluent(perm(Ev), Ins)  :- institution(Ins), eventType(Ev, Ins, inst).
inertialFluent(pow(Ev), Ins)   :- institution(Ins), eventType(Ev, Ins, inst).

% Null permissions hold from the start
holdsat(perm(null), Ins, I)    :- start(I), institution(Ins).
holdsat(pow(null),  Ins, I)    :- start(I), institution(Ins).

% Institutions also hold by default at the start:
% (which includes bridges, because they are institutions)
inertialFluent(live(Ins), Ins) :- institution(Ins).
holdsat(live(Ins), Ins, I)     :- start(I), institution(Ins).

% Reject all inertialFluent changes that aren't well formed:
:- inertialFluentChange(_, _, _, T), not inertialFluentChangeTypes(T).
:- inertialFluentChange(F, _, _, _), not inertialFluent(F, _).

%%-- end fluent rules
