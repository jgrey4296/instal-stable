%% null event for unknown events
% Event: null (type: ex)
event(null).
event(viol(null)).

evtype(null, ${inst}, ex).
evtype(viol(null), ${inst}, viol).

evinst(null, ${inst}).
evinst(viol(null), ${inst}).

ifluent(pow(null), ${inst}).
ifluent(perm(null), ${inst}).
fluent(pow(null), ${inst}).
fluent(perm(null), ${inst}).

% no creation event
holdsat(live(${inst}), ${inst}, I) :- start(I), inst(${inst}).
holdsat(perm(null), ${inst}, I)    :- start(I), inst(${inst}).
holdsat(pow(null), ${inst}, I)     :- start(I), inst(${inst}).
