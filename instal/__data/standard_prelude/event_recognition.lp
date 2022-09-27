%%-- events recognition
% Take Events that have been observed independent of institutions
% and interpret them into institutional events and fluents

%% Institutional null occurrence when nothing can be recognised:
occurred(null, In, I)          :- observed(E, I), instant(I), inst(In), not eventType(E, In, ex).

%% All Event Types define events:
event(Ev)                      :- eventType(Ev, _, _).

% All institutions have a null event type:
eventType(null, Ins, inst)     :- inst(Ins).

% All Events are associated with institutions
eventInst(Ev, Ins)             :- eventType(Ev, Ins, _).

% every insitutional action has a (potential) violation:
event(viol(Ev))                :- event(Ev), eventType(Ev, _, inst).
eventType(viol(Ev), Ins, viol) :- event(Ev), eventType(Ev, Ins, inst).

%% for Debugging:
% an unempowered event happens when an observed event does nothing to
% the institution
occurred(_unempoweredEvent(E), In, I)  :- eventType(E, In, ex), instant(I), inst(In), occurred(null, In, I), not observed(null, I).

% unrecognised happens when something is observed, but its not
% an external action the inst knows
occurred(_unrecognisedEvent(E), In, I) :- observed(E, I), instant(I), inst(In), not eventType(E, In, ex).


%% Reject any model with a faulty event type:
:- eventType(_, _, T), not event_types(T).

%%-- end events recognition
