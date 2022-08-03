%% cross generate rules %
%%
% Translation of ${event} of ${source} xgenerates ${response} of ${sink} if ${condition} in ${delay}\n
occurred(${response}, ${sink}, I${delay}) :-
  occurred(${event}, ${source}, I),
  holdsat(gpow(${source}, ${response}, ${sink}), ${bridge}, I${delay}),
  bridge(${bridge},  ${source},  ${sink})
  instant(I),
  ${rhs}.
