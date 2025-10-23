% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% InstAL Standard Prelude
% Sets up base rules for time, fluents,
% external fluents, events, violation rules.

% Guards against ungrounded institutions,
% supresses some clingo warnings
% and sets printed output
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#const horizon = 5.

% TODO: Remove the need for this in constraint generation
true.

%%-- suppress_warnings
ifluent(0,0).
nifluent(0,0).
oblfluent(0,0).
initiated(0,0,0).
xinitiated(0,0,0,0).
terminated(0,0,0).
xterminated(0,0,0,0).
_typeNotDeclared :- 1 == 2.
bridge(1).
%%-- end suppress_warnings

%%-- time
start(0).
final(horizon).
instant(0..T) :- final(T).
next(T,T+1) :- instant(T).
%%-- end time

%%-- fluent rules
fluentterminated(P, In, I) :- terminated(P, In, I), instant(I), inst(In).
fluentterminated(P, In, I) :- xterminated(InS, P, In, I), instant(I), inst(In), inst(InS).

fluentinitiated(P, In, I) :- initiated(P, In, I), instant(I), inst(In).
fluentinitiated(P, In, I) :- xinitiated(InSo, P, In, I), inst(InSo), inst(In), instant(I).

holdsat(P,In,J):- holdsat(P,In,I),not fluentterminated(P,In,I),
	next(I,J),ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- fluentinitiated(P,In,I),next(I,J),
	ifluent(P, In),instant(I),instant(J), inst(In).

holdsat(P,In,J):- holdsat(P,In,I),not fluentterminated(P,In,I),
	next(I,J),ifluent(P, In),instant(I),instant(J), bridge(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
	ifluent(P, In),instant(I),instant(J), bridge(In).
%%-- end fluent rules

%%-- external fluent rules
#external holdsat(F,I) : ifluent(F,I), inst(I).
holdsat(F,I,J) :- holdsat(F,I), start(J).
%%-- end external fluent rules

%%-- events occur
occurred(E,In,I):- eventType(E,In,ex),observed(E,In,I),instant(I), inst(In), holdsat(pow(E), In, I).
occurred(_unempoweredEvent(E), In, I) :- eventType(E,In,ex),observed(E,In,I),instant(I), inst(In), not holdsat(pow(E), In, I).
occurred(_unrecognisedEvent(E),In,I) :- not eventType(E,In,ex), observed(E,In,I),
	instant(I), inst(In).

occurred(null,In,I) :- not eventType(E,In,ex), observed(E,In,I),
	instant(I), inst(In). % TODO: What's the point of the null anyway?
%%-- end events occur

%%-- event set
#external _eventSet(I) : instant(I).
%%-- end event set

%%-- observation sequences
#external extObserved(E,I) : event(E), eventType(E,_,ex), instant(I).

recEvent(I) :- extObserved(E, I), event(E), instant(I), not final(I).
extObserved(_unrecognisedEvent, I) :- not recEvent(I), _eventSet(I).
%%-- end observation sequences

%%-- violations for non-permitted events
occurred(viol(E),In,I):-
	occurred(E,In,I),
	not holdsat(perm(E),In,I),
	holdsat(live(In),In,I),
	eventInst(E,In),
	event(E),
	instant(I),
	event(viol(E)),inst(In).
%%-- end violations for non-permitted events

%%-- mode COMPOSITE is chosen
1 {genObserved(E, J) : eventType(E, In, ex), inst(In)} 1 :-
	instant(J),
	not final(J),
	not extObserved(_, J).

:- observed(E,J),
	 observed(F,J),
	 instant(J),
	 eventType(E,InX,ex),
   eventType(F,InY,ex),
	 E!=F,
	 inst(InX;InY).

obs(I):- observed(_,I),instant(I).

:- not obs(I), not final(I), instant(I), inst(In).
observed(E, I)		:- genObserved(E, I), not final(I).
observed(E, I)		:- extObserved(E, I), not final(I).
observed(E,In,I)	:- observed(E,I), inst(In), instant(I).
%%-- end mode COMPOSITE is chosen

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

%%-- output control
#show observed/2.
#show occurred/3.
#show holdsat/3.
%%-- end output control

_preludeLoaded.
