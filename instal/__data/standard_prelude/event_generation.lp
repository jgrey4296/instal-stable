%%-- mode COMPOSITE is chosen
1 {genObserved(E, J) : evtype(E, In, ex), inst(In)} 1 :-
	instant(J),
	not final(J),
	not extObserved(_, J).

:- observed(E, J),
	 observed(F, J),
	 instant(J),
	 evtype(E, InX, ex),
   evtype(F, InY, ex),
	 E!=F,
	 inst(InX;InY).

obs(I) :- observed(_, I), instant(I).
:- instant(I), inst(In), not obs(I), not final(I).

observed(E, I)     :- genObserved(E, I), not final(I).
observed(E, I)     :- extObserved(E, I), not final(I).
observed(E, In, I) :- observed(E, I), inst(In), instant(I).
%%-- end mode COMPOSITE is chosen
