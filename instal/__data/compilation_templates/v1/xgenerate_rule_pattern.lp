% Translation of ${event} of ${source} xgenerates ${response} of ${sink} if [condition] in ${delay}
occurred(${response}, ${sink}, I${delay}) :- instant(I),
                                             bridge(${bridge},  ${source},  ${sink})
                                             holdsat(gpow(${source}, ${response}, ${sink}), ${bridge}, I${delay}),
                                             occurred(${event}, ${source}, I),
                                             ${rhs}.
