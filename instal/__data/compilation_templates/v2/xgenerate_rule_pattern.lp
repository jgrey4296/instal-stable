% Translation of ${event} of ${source} xgenerates ${response} of ${sink} if [condition] in ${delay}
occurred(${response}, ${sink}, I${delay}) :- instant(I),
                                             bridge(${bridge},  ${source},  ${sink}),
                                             holdsat(deontic(genPow, ev(${source}, ${response}, ${sink})), ${bridge}, I),
                                             occurred(${event}, ${source}, I),
                                             ${rhs}.
