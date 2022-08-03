% Event: ${event} (type: exogenous)
event(${event})                       :- ${rhs}.
event(viol(${event}))                 :- ${rhs}.

evtype(${event}, ${inst}, ex)         :- ${rhs}.
evtype(viol(${event}), ${inst}, viol) :- ${rhs}.

evinst(${event}, ${inst})             :- ${rhs}.
evinst(viol(${event}), ${inst})       :- ${rhs}.

fluent(pow(${event}), ${inst})        :- ${rhs}.
fluent(perm(${event}), ${inst})       :- ${rhs}.

ifluent(pow(${event}), ${inst})       :- ${rhs}.
ifluent(perm(${event}), ${inst})      :- ${rhs}.
