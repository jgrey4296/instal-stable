%% obligation fluent: ${fluent} %
ofluent(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst})  :- institution(${inst}),
                                                                                ${rhs}.


% Do the obligation (inst) event:
occurred(obl(${obligation}), ${inst}, I) :- institution(${inst}),
                                            eventType(${obligation}, ${inst}, inst),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            occured(${obligation}, Ins, I),
                                            ${rhs}.

% Do the obligation (ex) event:
occurred(obl(${obligation}), ${inst}, I) :- institution(${inst}),
                                            eventType(${obligation}, ${inst}, ex),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            observed(${obligation}, I),
                                            ${rhs}.

% bring about the obligation state:
occurred(obl(${obligation}), ${inst}, I) :- institution(${inst}),
                                            fluent(${obligation}),
                                            holdsat(${obligation}, ${inst}, I),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            ${rhs}.

% trigger a violation if the violating (inst) event occurs:
occurred(viol(${violation}), ${inst}, I) :- institution(${inst}),
                                            event(${violation}),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            occurred(${violation}, ${inst}, I),
                                            ${rhs}.

% trigger a violation if the violating (ex) event occurs:
occurred(viol(${violation}), ${inst}, I) :- institution(${inst}),
                                            event(${violation}),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            observed(${violation}, I),
                                            ${rhs}.

% trigger a violation if the the violating state occurs:
occurred(viol(${violation}), ${inst}, I) :- institution(${inst}),
                                            fluent(${violation}),
                                            holdsat(${violation}, ${inst}, I),
                                            holdsat(obl(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                            ${rhs}.
