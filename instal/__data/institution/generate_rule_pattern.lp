% Translation of ${event} generates ${state} if [condition] (in ${delay})
occurred(${state}, ${inst}, I${delay})         :- observed(${event}, I),
                                                  inst(${inst}),
                                                  instant(I),
                                                  eventType(${state}, ${inst}, inst),
                                                  eventType(${event}, ${inst}, ex),
                                                  holdsat(perm(${state}), ${inst}, I),
                                                  not occurred(viol(${state}), ${inst}, I),
                                                  ${rhs}.

occurred(_unpermittedEvent(${state}), ${inst}, I) :-  observed(${event}, I),
                                                      inst(${inst}),
                                                      instant(I),
                                                      eventType(${state}, ${inst}, inst),
                                                      eventType(${event}, ${inst}, ex),
                                                      not holdsat(perm(${state}), ${inst}, I),
                                                      ${rhs}.


% chain_occurred(${state}, ${inst}, ${event}, I) :- occurred(${event}, ${inst}, I),
%                                                   inst(${inst}),
%                                                   instant(I),
%                                                   eventType(${state}, ${inst}, inst),
%                                                   eventType(${event}, ${inst}, inst),
%                                                   not occurred(viol(${event}, ${inst}, I)),
%                                                   ${rhs}.

% occurred(${state}, ${inst}, I${delay})         :- chain_occurred(${state}, ${inst}, _, I).
