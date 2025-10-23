% Event: ${event} (type: institutional)
event(${event})                          :- ${rhs}.
event(viol(${event}))                    :- ${rhs}.

eventType(${event}, ${inst}, inst)       :- ${rhs}.
eventType(viol(${event}), ${inst}, viol) :- ${rhs}.

eventInst(${event}, ${inst})             :- ${rhs}.
eventInst(viol(${event}), ${inst})       :- ${rhs}.

ifluent(perm(${event}), ${inst})         :- ${rhs}.
fluent(perm(${event}), ${inst})          :- ${rhs}.
