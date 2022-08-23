%%-- violations for non-permitted events
occurred(viol(E), In, I):-
	occurred(E, In, I),
	holdsat(live(In), In, I),
	eventInst(E, In),
	event(E),
	instant(I),
	event(viol(E)),
	inst(In),
	not holdsat(perm(E), In, I) .
%%-- end violations for non-permitted events
