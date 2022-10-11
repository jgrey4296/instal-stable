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
event(violation(Ev))                   :- event(Ev), eventType(Ev, _,   inst).
eventType(violation(Ev), Ins, viol)    :- event(Ev), eventType(Ev, Ins, inst).

%% Institutional null occurrence when nothing can be recognised:
{ occurred(null, In, I) }             :- instant(I),
                                         institution(In),
                                         not occurred(_, I).


%% for Debugging:
% an unempowered event happens when an observed event does nothing to
% the institution
occurred(_unempoweredEvent(E), In, I)  :- instant(I),
                                          institution(In),
                                          eventType(E, In, ex),
                                          observed(E, I),
                                          occurred(null, In, I),
                                          E != null.

%% Reject any model with a faulty event type:
% :- eventType(_, _, T), not event_types(T).

:- instant(I), institution(In), not occurred(_, In, I).

%%-- end events recognition
