%% obligation fluent: ${fluent} %
obligationalFluent(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}) :- institution(${inst}),
                                                                                                  ${rhs}.


% Do the obligation (inst) event:
occurred(obligation(${obligation}), ${inst}, I) :- institution(${inst}),
                                                   eventType(${obligation}, ${inst}, inst),
                                                   holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                   occurred(${obligation}, Ins, I),
                                                   ${rhs}.

% Do the obligation (ex) event:
occurred(obligation(${obligation}), ${inst}, I) :- institution(${inst}),
                                                   eventType(${obligation}, ${inst}, ex),
                                                   holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                   observed(${obligation}, I),
                                                   ${rhs}.

% bring about the obligation state:
occurred(obligation(${obligation}), ${inst}, I) :- institution(${inst}),
                                                   fluent(${obligation}),
                                                   holdsat(${obligation}, ${inst}, I),
                                                   holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                   ${rhs}.

% trigger a violation if the violating (inst) event occurs:
occurred(violation(${violation}), ${inst}, I) :- institution(${inst}),
                                                 event(${violation}),
                                                 holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                 occurred(${violation}, ${inst}, I),
                                                 ${rhs}.

% trigger a violation if the violating (ex) event occurs:
occurred(violation(${violation}), ${inst}, I) :- institution(${inst}),
                                                 event(${violation}),
                                                 holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                 observed(${violation}, I),
                                                 ${rhs}.

% trigger a violation if the the violating state occurs:
occurred(violation(${violation}), ${inst}, I) :- institution(${inst}),
                                                 fluent(${violation}),
                                                 holdsat(${violation}, ${inst}, I),
                                                 holdsat(obligation(${obligation}, ${deadline}, ${violation}, ${repeats}), ${inst}, I),
                                                 ${rhs}.
