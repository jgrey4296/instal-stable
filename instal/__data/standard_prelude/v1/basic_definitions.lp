
%%-- core types
eventTypes(ex;viol;inst).
fluentTypes(inertial;transient;obligation).
inertialFluentChangeTypes(initiated;terminated).
obligationTypes(oneshot;multishot).
%%-- end core types

%%-- output control
#show observed/2.
#show occurred/3.
#show holdsat/3.
#show institution/1.
#show bridge/3.
%%-- end output control

%%-- external manipulation
% how many timesteps there are available.
#const    horizon = 5.

% dictate events that happen at certain timesteps
#external extObserved(E, I)  : eventType(E, _, ex), instant(I).
% this allows to guard against bad extObserved settings:
% (see unrecognised events)
#external _eventSet(I)       : instant(I).
% dictate fluents that hold at certain timesteps
#external extHoldsat(F, I)   : inertialFluent(F, I), institution(I).
%%-- end external manipulation

%%-- suppress_warnings
true.
event(null).
event(violation(null)).
inertialFluent(0, 0).
transientFluent(0, 0).
obligationalFluent(0, 0).
initiated(0, 0, 0).
terminated(0, 0, 0).
xInitiated(0, 0, 0, 0).
xTerminated(0, 0, 0, 0).
bridge(0,0,0).
sink(0, 0).
source(0, 0).
_typeNotDeclared :- 1 == 2.
%%-- end suppress_warnings

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

_preludeLoaded.
