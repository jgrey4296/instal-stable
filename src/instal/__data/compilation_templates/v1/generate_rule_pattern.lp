% Translation of ${event} generates ${state} if [condition] (in ${delay})
occurred(${state}, ${inst}, I${delay}) :- occurred(${event}, ${inst}, I), inst(${inst}), instant(I), not occurred(viol(${event}), ${inst}, I), ${rhs}.
