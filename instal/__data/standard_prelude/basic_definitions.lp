
%%-- core types
event_types(ex;viol;inst).
fluent_types(inertial;noninertial;obligation).
ifluent_changes(initiated;terminated).
obligation_types(oneshot;multishot).

%%-- end core types


%%-- output control
#show observed/2.
#show occurred/3.
#show holdsat/3.
#show inst/1.
%%-- end output control

%%-- external manipulation
% how many timesteps there are available.
#const    horizon = 5.

% dictate events that happen at certain timesteps
#external _eventSet(I) : instant(I).
#external extObserved(E, I) : event(E), eventType(E, _, ex), instant(I).

% dictate fluents that hold at certain timesteps
#external extHoldsat(F, I) : ifluent(F, I), inst(I).
%%-- end external manipulation

%%-- suppress_warnings
true.
event(null).
event(viol(null)).
ifluent(0, 0).
nifluent(0, 0).
ofluent(0, 0).
initiated(0, 0, 0).
terminated(0, 0, 0).
xinitiated(0, 0, 0, 0).
xterminated(0, 0, 0, 0).
bridge(0,0,0).
sink(0, 0).
source(0, 0).
_typeNotDeclared :- 1 == 2.
%%-- end suppress_warnings

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

_preludeLoaded.
