%% obligation fluent: ${fluent} %
ofluent(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst})  :- inst(${inst}),
                                                                                ${rhs}.


% Do the obligation (inst) event:
occurred(obl(${obligation}), ${inst}, I) :- inst(${inst}),
                                            eventType(${obligation}, ${inst}, inst),
                                            occured(${obligation}, Ins, I),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            ${rhs}.

% Do the obligation (ex) event:
occurred(obl(${obligation}), ${inst}, I) :- inst(${inst}),
                                            eventType(${obligation}, ${inst}, ex),
                                            observed(${obligation}, I),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            ${rhs}.

% bring about the obligation state:
occurred(obl(${obligation}), ${inst}, I) :- inst(${inst}),
                                            fluent(${obligation}),
                                            holdsat(${obligation}, ${inst}, I),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            ${rhs}.

% trigger a violation if the violating (inst) event occurs:
occurred(viol(${violation}), ${inst}, I) :- inst(${inst}),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            event(${violation}),
                                            occurred(${violation}, ${inst}, I),
                                            ${rhs}.

% trigger a violation if the violating (ex) event occurs:
occurred(viol(${violation}), ${inst}, I) :- inst(${inst}),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            event(${violation}),
                                            observed(${violation}, I),
                                            ${rhs}.

% trigger a violation if the the violating state occurs:
occurred(viol(${violation}), ${inst}, I) :- inst(${inst}),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            fluent(${violation}),
                                            holdsat(${violation}, ${inst}, I),
                                            ${rhs}.
