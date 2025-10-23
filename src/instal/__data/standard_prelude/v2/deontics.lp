%%-- deontics
% All Institutions have norm fluents for all institution events
inertialFluent(deontic(D, Ev), Ins) :- institution(Ins), deonticTypes(D), eventType(Ev, Ins, inst).

% Null permissions hold from the start
inertialFluent(deontic(D, null), Ins) :- institution(Ins), deonticTypes(D), eventType(Ev, Ins, inst).

holdsat(deontic(D, null), Ins, I) :- start(I), institution(Ins), deonticTypes(D).
%%-- end deontics
