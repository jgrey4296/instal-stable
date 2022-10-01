ifluent(gpow(${source}, ${event},  ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}),
                                                           eventType(${event}, ${sink}, ex),
                                                           ${rhs}.
