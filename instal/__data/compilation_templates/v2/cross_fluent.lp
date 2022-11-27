inertialFluent(deontic(${power}, ev(${source}, ${fluent}, ${sink})), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}),
                                                                                   inertialFluent(${fluent}, ${sink}),
                                                                                   ${rhs}.
