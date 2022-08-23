fluent(gpow(${source},  ${event},  ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}), eventInst(${event}, ${sink}), eventType(${event}, ${sink}, ex), ${rhs}.
ifluent(gpow(${source}, ${event},  ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}), eventInst(${event}, ${sink}), eventType(${event}, ${sink}, ex), ${rhs}.
