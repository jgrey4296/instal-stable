%%-- fluent rules
fluentterminated(P, In, I)	:- terminated(P, In, I), instant(I), inst(In).
fluentterminated(P, In, I)	:- xterminated(InS, P, In, I), instant(I), inst(In), inst(InS).

fluentinitiated(P, In, I)		:- initiated(P, In, I), instant(I), inst(In).
fluentinitiated(P, In, I)		:- xinitiated(InSo, P, In, I), inst(InSo), inst(In), instant(I).

holdsat(P, In, J)						:- holdsat(P, In, I), next(I, J), ifluent(P, In), instant(I), instant(J), inst(In), not fluentterminated(P, In, I).

holdsat(P, In, J)						:- fluentinitiated(P, In, I), next(I, J), ifluent(P, In), instant(I), instant(J), inst(In).
%%-- end fluent rules

%%-- external fluent rules
#external holdsat(F, I) : ifluent(F, I), inst(I).
holdsat(F, I, J)						:- holdsat(F, I), start(J).
%%-- end external fluent rules
