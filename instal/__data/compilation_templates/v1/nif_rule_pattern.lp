%% Translation of ${state} when ${rhs}
holdsat(${state}, ${inst}, I) :- inst(${inst}), instant(I), ${rhs}.
