true.

%%-- suppress_warnings
event_type(ex;viol;inst).

ifluent(0, 0).
nifluent(0, 0).
oblfluent(0, 0).
initiated(0, 0, 0).
terminated(0, 0, 0).
xinitiated(0, 0, 0, 0).
xterminated(0, 0, 0, 0).
bridge(1).
_typeNotDeclared :- 1 == 2.
%%-- end suppress_warnings

%%-- defends against partially grounded institutions
:- _typeNotDeclared.
%%-- end defends against partially grounded institutions

%%-- output control
#show observed/2.
#show occurred/3.
#show holdsat/3.
%%-- end output control

_preludeLoaded.
