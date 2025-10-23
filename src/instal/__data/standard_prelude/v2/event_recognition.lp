%%-- events recognition
% Take Events that have been observed independent of institutions
% and interpret them into institutional events and fluents

%% All Event Types define events:
event(Ev)                         :- eventType(Ev, _, _).

% All institutions have a null event type:
eventType(null, Ins, inst)        :- institution(Ins).

% All Events are associated with institutions
eventInst(Ev, Ins)                :- eventType(Ev, Ins, _).

% every insitutional action has a (potential) violation:
eventType(violation(Ev), Ins, viol)    :- eventType(Ev, Ins, inst).

%% Institutional null occurrence when nothing can be recognised:
{ occurred(null, In, I) }             :- instant(I),
                                         institution(In),
                                         not occurred(_, I).


%% Reject any model with a faulty event type:
:- eventType(_, _, T), not eventTypes(T).
% Reject any model where nothing happens on a timestep
:- instant(I), institution(In), not occurred(_, In, I).

%%-- end events recognition
