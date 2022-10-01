%% Translation of ${event} initiates ${state} if [condition]
initiated(${state}, ${inst}, I) :- occurred(${event}, ${inst}, I), holdsat(live(${inst}), ${inst}, I), inst(${inst}), instant(I), not occurred(viol(${event}), ${inst}, I), ${rhs}.
