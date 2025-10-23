% Event: ${event} (type: exogenous)
event(${event})                       :- ${rhs}.
event(viol(${event}))                 :- ${rhs}.

eventType(${event}, ${inst}, ex)         :- ${rhs}.
eventType(viol(${event}), ${inst}, viol) :- ${rhs}.

eventInst(${event}, ${inst})             :- ${rhs}.
eventInst(viol(${event}), ${inst})       :- ${rhs}.

fluent(pow(${event}), ${inst})        :- ${rhs}.
fluent(perm(${event}), ${inst})       :- ${rhs}.

ifluent(pow(${event}), ${inst})       :- ${rhs}.
ifluent(perm(${event}), ${inst})      :- ${rhs}.
