% Event: ${event} (type: institutional)
event(${event})                       :- ${rhs}.
event(viol(${event}))                 :- ${rhs}.

evtype(${event}, ${inst}, inst)       :- ${rhs}.
evtype(viol(${event}), ${inst}, viol) :- ${rhs}.

evinst(${event}, ${inst})             :- ${rhs}.
evinst(viol(${event}), ${inst})       :- ${rhs}.

ifluent(perm(${event}), ${inst})      :- ${rhs}.
fluent(perm(${event}), ${inst})       :- ${rhs}.
