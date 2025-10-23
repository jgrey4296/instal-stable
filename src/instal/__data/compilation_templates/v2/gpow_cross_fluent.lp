inertialFluent(deontic(genPower, ev(${source}, ${event}, ${sink})), ${bridge}) :- bridge(${bridge}, ${source}, ${sink}),
                                                                                  eventType(${event}, ${sink}, inst),
                                                                                  ${rhs}.
