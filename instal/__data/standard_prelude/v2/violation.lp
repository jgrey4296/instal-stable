%%-- violations for non-permitted events
% convert an event that lacks the permission for its performance,
% into an occurrence of a violation event
occurred(violation(E), In, I):- instant(I),
                                institution(In),
                                eventType(E, In, inst),
                                holdsat(live(In), In, I),
                                occurred(E, In, I),
                                not holdsat(perm(E), In, I).
%%-- end violations for non-permitted events
