:- not occurred(enterroom(_),_,_).
:- observed(null,T), instant(T).
:- occurred(_unempoweredEvent(_),_,_).
:- occurred(viol(_),_,_).

:~ occurred(rude(X),_,T), instant(T), person(X). [10]
:~ occurred(enterroom(_),_,T), instant(T). [T]
