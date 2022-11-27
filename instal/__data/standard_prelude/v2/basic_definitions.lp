
%%-- core types
eventTypes(ex;viol;inst).
fluentTypes(inertial;transient;obligation).
obligationTypes(achievement;maintenance).   % subtypes of obligations
inertialFluentChangeTypes(initiated;terminated).
deonticTypes(power;permitted;forbidden).    % basic deontics
deonticTypes(genPower;initPower;termPower). % bridge deontics
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
bridge(0,0,0)                             :- 1 == 2.
event(null)                               :- 1 == 2.
event(violation(null))                    :- 1 == 2.
eventType(0,0,0)                          :- 1 == 2.
inertialFluent(0, 0)                      :- 1 == 2.
initiated(0, 0, 0)                        :- 1 == 2.
obligationFluent(0, 0)                    :- 1 == 2.
obligationFluent(obligation(0,0,0,0),0)   :- 1 == 2.
occurred(obligation(0), 0, 0)             :- 1 == 2.
occurred(0, 0)                            :- 1 == 2.
occurred(0,0,0)                           :- 1 == 2.
sink(0, 0)                                :- 1 == 2.
source(0, 0)                              :- 1 == 2.
terminated(0, 0, 0)                       :- 1 == 2.
transientFluent(0, 0)                     :- 1 == 2.
xInitiated(0, 0, 0, 0)                    :- 1 == 2.
xTerminated(0, 0, 0, 0)                   :- 1 == 2.
_typeNotDeclared                          :- 1 == 2.
%%-- end suppress_warnings

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

_preludeLoaded.
