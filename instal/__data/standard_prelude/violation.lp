%%-- violations for non-permitted events
% convert an event that lacks the permission for its performance,
% into an occurrence of a violation event
occurred(viol(E), In, I):-
	occurred(E, In, I),
	holdsat(live(In), In, I),
	eventType(E, In, inst),
	instant(I),
	inst(In),
	not holdsat(perm(E), In, I) .
%%-- end violations for non-permitted events
