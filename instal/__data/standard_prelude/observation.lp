%%-- observation sequences
#external extObserved(E, I) : event(E), evtype(E, _, ex), instant(I).

recEvent(I)                        :- extObserved(E, I), event(E), instant(I), not final(I).
extObserved(_unrecognisedEvent, I) :- _eventSet(I), not recEvent(I).
%%-- end observation sequences
