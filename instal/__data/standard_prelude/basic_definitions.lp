
%%-- suppress_warnings
eventType(ex;viol;inst).

true.
ifluent(0, 0).
nifluent(0, 0).
oblfluent(0, 0).
initiated(0, 0, 0).
terminated(0, 0, 0).
xinitiated(0, 0, 0, 0).
xterminated(0, 0, 0, 0).
bridge(0,0,0).
_typeNotDeclared :- 1 == 2.
%%-- end suppress_warnings

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

%%-- output control
#show observed/2.
#show occurred/3.
#show holdsat/3.
#show inst/1.
%%-- end output control

_preludeLoaded.
