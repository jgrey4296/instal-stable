%%-- event observation
% The null event:
eventType(null, Ins, ex) :- inst(Ins).
% Generate 1 event per timestep, except steps where an event has been externally set/queried
1 {genObserved(E, J) : eventType(E, In, ex), inst(In)} 1 :-
   	instant(J),
	  not final(J),
	  not extObserved(_, J).

% Observe events set externally if they are valid, or register the conflict
recEvent(I)                        :- extObserved(E, I), event(E), instant(I), not final(I).
extObserved(_unrecognisedEvent, I) :- _eventSet(I), not recEvent(I).

% Flatten external and generated events into one type.
observed(E, I)     :- extObserved(E, I), not final(I).
observed(E, I)     :- genObserved(E, I), not final(I).

% Constrain models to have only 1 external event per timestep?
:- observed(E, J),
	 observed(F, J),
	 instant(J),
	 eventType(E, InX, ex),
   eventType(F, InY, ex),
	 E!=F,
	 inst(InX;InY).

% Constrain models to have no timesteps without events
obs(I) :- observed(_, I), instant(I).
:- instant(I), inst(In), not obs(I), not final(I).

%%-- end event observation

