%%-- violations for non-permitted events
% convert an event that lacks the permission for its performance,
% into an occurrence of a violation event
occurred(violation(E), In, I):- instant(I),
                                institution(In),
                                occurred(E, In, I),
                                holdsat(live(In), In, I),
                                eventType(E, In, inst),
                                not holdsat(perm(E), In, I).
%%-- end violations for non-permitted events
