fluent(${power}(${source}, ${fluent}, ${sink}), ${bridge})  :- bridge(${bridge}, ${source}, ${sink}), ${rhs}.
ifluent(${power}(${source}, ${fluent}, ${sink}), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}), ${rhs}.
