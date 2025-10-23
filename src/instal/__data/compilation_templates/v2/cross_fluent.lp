inertialFluent(deontic(${power}, ev(${source}, ${fluent}, ${sink})), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}),
                                                                                   bridgeDeonticTypes(${power}),
                                                                                   inertialFluent(${fluent}, ${sink}),
                                                                                   ${rhs}.
