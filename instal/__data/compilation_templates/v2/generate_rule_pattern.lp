% Translation of ${event} generates ${state} if [condition] (in ${delay})
%% Ex Event generates Inst Event:
occurred(${state}, ${inst}, I${delay})            :- instant(I),
                                                     institution(${inst}),
                                                     observed(${event}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, ex),
                                                     holdsat(perm(${state}), ${inst}, I),
                                                     not occurred(violation(${state}), ${inst}, I),
                                                     ${rhs}.
%% Inst Event Generates Inst Event
occurred(${state}, ${inst}, I${delay})            :- instant(I),
                                                     institution(${inst}),
                                                     occurred(${event}, ${inst}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, inst),
                                                     holdsat(perm(${state}), ${inst}, I),
                                                     not occurred(violation(${state}), ${inst}, I),
                                                     ${rhs}.

occurred(_unpermittedEvent(${state}), ${inst}, I) :- instant(I),
                                                     institution(${inst}),
                                                     observed(${event}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, _),
                                                     not holdsat(perm(${state}), ${inst}, I),
                                                     ${rhs}.

