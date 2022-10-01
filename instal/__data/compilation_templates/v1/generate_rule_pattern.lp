% Translation of ${event} generates ${state} if [condition] (in ${delay})
occurred(${state}, ${inst}, I${delay})            :- instant(I),
                                                     institution(${inst}),
                                                     observed(${event}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, ex),
                                                     holdsat(perm(${state}), ${inst}, I),
                                                     not occurred(violation(${state}), ${inst}, I),
                                                     ${rhs}.

occurred(_unpermittedEvent(${state}), ${inst}, I) :- instant(I),
                                                     institution(${inst}),
                                                     observed(${event}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, ex),
                                                     not holdsat(perm(${state}), ${inst}, I),
                                                     ${rhs}.


chain_occurred(${state}, ${inst}, ${event}, I)   :-  instant(I),
                                                     institution(${inst}),
                                                     occurred(${event}, ${inst}, I),
                                                     eventType(${state}, ${inst}, inst),
                                                     eventType(${event}, ${inst}, inst),
                                                     not occurred(violation(${event}, ${inst}, I)),
                                                     ${rhs}.

% occurred(${state}, ${inst}, I${delay})         :- chain_occurred(${state}, ${inst}, _, I).
