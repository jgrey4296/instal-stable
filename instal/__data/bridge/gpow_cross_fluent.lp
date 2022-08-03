fluent(gpow(${source},  ${event},  ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}), evinst(${event}, ${sink}), evtype(${event}, ${sink}, ex), ${rhs}.
ifluent(gpow(${source}, ${event},  ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}), evinst(${event}, ${sink}), evtype(${event}, ${sink}, ex), ${rhs}.
