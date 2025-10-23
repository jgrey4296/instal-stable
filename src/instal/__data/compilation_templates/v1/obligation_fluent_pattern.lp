%% obligation fluent: ${fluent} %
oblfluent(obl(${obligation}, ${deadline}, ${violation}), ${inst})     :- inst(${inst}), event(${violation}), ${rhs}.
ifluent(obl(${obligation}, ${deadline}, ${violation}), ${inst})       :- inst(${inst}), event(${violation}), ${rhs}.
fluent(obl(${obligation}, ${deadline}, ${violation}), ${inst})        :- inst(${inst}), event(${violation}), ${rhs}.
terminated(obl(${obligation}, ${deadline}, ${violation}), ${inst}, I) :- inst(${inst}), holdsat(obl(${obligation}, ${deadline}, ${violation}), ${inst}, I), event(${violation}), ${rhs}.
terminated(obl(${obligation}, ${deadline}, ${violation}), ${inst}, I) :- inst(${inst}), holdsat(obl(${obligation}, ${deadline}, ${violation}), ${inst}, I), event(${violation}), ${rhs}.
occurred(${violation}, ${inst}, I)                                    :- inst(${inst}), holdsat(obl(${obligation}, ${deadline}, ${violation}), ${inst}, I), event(${violation}), ${rhs}.
