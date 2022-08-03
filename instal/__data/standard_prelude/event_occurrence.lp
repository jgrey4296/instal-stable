%%-- events occur
occurred(E, In, I)										 :- evtype(E, In, ex), observed(E, In, I), instant(I), inst(In), holdsat(pow(E), In, I).

occurred(_unempoweredEvent(E), In, I)  :- evtype(E, In, ex), observed(E, In, I), instant(I), inst(In), not holdsat(pow(E), In, I).

occurred(_unrecognisedEvent(E), In, I) :- observed(E, In, I), instant(I), inst(In), not evtype(E, In, ex).

occurred(null, In, I)									 :- observed(E, In, I), instant(I), inst(In) not evtype(E, In, ex).
%%-- end events occur

%%-- event set
#external _eventSet(I) : instant(I).
%%-- end event set
