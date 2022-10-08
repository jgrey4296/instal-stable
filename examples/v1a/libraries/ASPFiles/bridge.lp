%
% Domain declarations for bridge
%
inst(pubA).
inst(libB).
inst(libC).
inst(bridge).
user(alice).
user(bob).
book(book1_a).
book(book2_a).
book(book3_a).
book(book4_a).
book(book1_b).
book(book2_b).
book(book1_c).
book(book2_c).
number(0).
number(1).
number(2).
number(3).
number(4).
number(5).
%
% -------------------------------PART 1-------------------------------
%
%
% Standard prelude for bridge
%
% fluent rules
holdsat(P,In,J):- holdsat(P,In,I),not terminated(P,In,I), not xterminated(InS,P,In,I), 
    next(I,J),ifluent(P, In),instant(I),instant(J), inst(In;InS).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
    ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J), 
    oblfluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J), 
    nifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J),
    ifluent(P, In),instant(I),instant(J), inst(InS;In).
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J), 
    oblfluent(P, In),instant(I),instant(J), inst(InS;In).
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J), 
    nifluent(P, In),instant(I),instant(J), inst(InS;In).
true.
%
% Rules for Institution bridge
%
  ifluent(live(bridge), bridge).
  fluent(live(bridge), bridge).
  inst(bridge).
%
% The following types were declared:
%
% Book
% Inst
% User
% Number
%
% Exogenous events
% Event: register (type: ex) of institution libC
  event(register(User0)) :- user(User0).
  evtype(register(User0),libC,ex) :- user(User0).
  evinst(register(User0),libC) :- user(User0).
  ifluent(perm(register(User0)), libC) :- user(User0).
  fluent(perm(register(User0)), libC) :- user(User0).
  event(viol(register(User0))) :- user(User0).
  evtype(viol(register(User0)), libC, viol) :- user(User0).
  evinst(viol(register(User0)),libC) :- user(User0).
% Event: register (type: ex) of institution libB
  event(register(User0)) :- user(User0).
  evtype(register(User0),libB,ex) :- user(User0).
  evinst(register(User0),libB) :- user(User0).
  ifluent(perm(register(User0)), libB) :- user(User0).
  fluent(perm(register(User0)), libB) :- user(User0).
  event(viol(register(User0))) :- user(User0).
  evtype(viol(register(User0)), libB, viol) :- user(User0).
  evinst(viol(register(User0)),libB) :- user(User0).
% Event: register (type: ex) of institution pubA
  event(register(User0)) :- user(User0).
  evtype(register(User0),pubA,ex) :- user(User0).
  evinst(register(User0),pubA) :- user(User0).
  ifluent(perm(register(User0)), pubA) :- user(User0).
  fluent(perm(register(User0)), pubA) :- user(User0).
  event(viol(register(User0))) :- user(User0).
  evtype(viol(register(User0)), pubA, viol) :- user(User0).
  evinst(viol(register(User0)),pubA) :- user(User0).
% Event: rmBorrow (type: ex) of institution libC
  event(rmBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(rmBorrow(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(rmBorrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(rmBorrow(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(rmBorrow(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(rmBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(rmBorrow(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(rmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: rmBorrow (type: ex) of institution libB
  event(rmBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(rmBorrow(User0,Book1),libB,ex) :- user(User0),book(Book1).
  evinst(rmBorrow(User0,Book1),libB) :- user(User0),book(Book1).
  ifluent(perm(rmBorrow(User0,Book1)), libB) :- user(User0),book(Book1).
  fluent(perm(rmBorrow(User0,Book1)), libB) :- user(User0),book(Book1).
  event(viol(rmBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(rmBorrow(User0,Book1)), libB, viol) :- user(User0),book(Book1).
  evinst(viol(rmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
% Event: borrow (type: ex) of institution libC
  event(borrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(borrow(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(borrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(borrow(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(borrow(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(borrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(borrow(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(borrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: borrow (type: ex) of institution libB
  event(borrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(borrow(User0,Book1),libB,ex) :- user(User0),book(Book1).
  evinst(borrow(User0,Book1),libB) :- user(User0),book(Book1).
  ifluent(perm(borrow(User0,Book1)), libB) :- user(User0),book(Book1).
  fluent(perm(borrow(User0,Book1)), libB) :- user(User0),book(Book1).
  event(viol(borrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(borrow(User0,Book1)), libB, viol) :- user(User0),book(Book1).
  evinst(viol(borrow(User0,Book1)),libB) :- user(User0),book(Book1).
% Event: borrow (type: ex) of institution pubA
  event(borrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(borrow(User0,Book1),pubA,ex) :- user(User0),book(Book1).
  evinst(borrow(User0,Book1),pubA) :- user(User0),book(Book1).
  ifluent(perm(borrow(User0,Book1)), pubA) :- user(User0),book(Book1).
  fluent(perm(borrow(User0,Book1)), pubA) :- user(User0),book(Book1).
  event(viol(borrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(borrow(User0,Book1)), pubA, viol) :- user(User0),book(Book1).
  evinst(viol(borrow(User0,Book1)),pubA) :- user(User0),book(Book1).
% Event: rmRegister (type: ex) of institution libC
  event(rmRegister(User0)) :- user(User0).
  evtype(rmRegister(User0),libC,ex) :- user(User0).
  evinst(rmRegister(User0),libC) :- user(User0).
  ifluent(perm(rmRegister(User0)), libC) :- user(User0).
  fluent(perm(rmRegister(User0)), libC) :- user(User0).
  event(viol(rmRegister(User0))) :- user(User0).
  evtype(viol(rmRegister(User0)), libC, viol) :- user(User0).
  evinst(viol(rmRegister(User0)),libC) :- user(User0).
% Event: rmRegister (type: ex) of institution libB
  event(rmRegister(User0)) :- user(User0).
  evtype(rmRegister(User0),libB,ex) :- user(User0).
  evinst(rmRegister(User0),libB) :- user(User0).
  ifluent(perm(rmRegister(User0)), libB) :- user(User0).
  fluent(perm(rmRegister(User0)), libB) :- user(User0).
  event(viol(rmRegister(User0))) :- user(User0).
  evtype(viol(rmRegister(User0)), libB, viol) :- user(User0).
  evinst(viol(rmRegister(User0)),libB) :- user(User0).
%
% null event for unknown events
% Event: null (type: ex)
  event(null).
  evtype(null,bridge,ex).
  evinst(null,bridge).
  ifluent(perm(null), bridge).
  fluent(perm(null), bridge).
  event(viol(null)).
  evtype(viol(null),bridge,viol).
  evinst(viol(null),bridge).
% Institutional events
% Event: intRmRegister (type: in) of institution libC
  event(intRmRegister(User0)) :- user(User0).
  evtype(intRmRegister(User0),libC,inst) :- user(User0).
  evinst(intRmRegister(User0),libC) :- user(User0).
  ifluent(pow(libC,intRmRegister(User0)),libC) :- user(User0).
  ifluent(perm(intRmRegister(User0)),libC) :- user(User0).
  fluent(pow(libC,intRmRegister(User0)),libC) :- user(User0).
  fluent(perm(intRmRegister(User0)),libC) :- user(User0).
  event(viol(intRmRegister(User0))) :- user(User0).
  evtype(viol(intRmRegister(User0)),libC,viol) :- user(User0).
  evinst(viol(intRmRegister(User0)),libC) :- user(User0).
% Event: intRmRegister (type: in) of institution libB
  event(intRmRegister(User0)) :- user(User0).
  evtype(intRmRegister(User0),libB,inst) :- user(User0).
  evinst(intRmRegister(User0),libB) :- user(User0).
  ifluent(pow(libB,intRmRegister(User0)),libB) :- user(User0).
  ifluent(perm(intRmRegister(User0)),libB) :- user(User0).
  fluent(pow(libB,intRmRegister(User0)),libB) :- user(User0).
  fluent(perm(intRmRegister(User0)),libB) :- user(User0).
  event(viol(intRmRegister(User0))) :- user(User0).
  evtype(viol(intRmRegister(User0)),libB,viol) :- user(User0).
  evinst(viol(intRmRegister(User0)),libB) :- user(User0).
% Event: intRmRequest (type: in) of institution libC
  event(intRmRequest(User0,Book1)) :- user(User0),book(Book1).
  evtype(intRmRequest(User0,Book1),libC,inst) :- user(User0),book(Book1).
  evinst(intRmRequest(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(pow(libC,intRmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
  ifluent(perm(intRmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(pow(libC,intRmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(perm(intRmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
  event(viol(intRmRequest(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intRmRequest(User0,Book1)),libC,viol) :- user(User0),book(Book1).
  evinst(viol(intRmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: intRmRequest (type: in) of institution libB
  event(intRmRequest(User0,Book1)) :- user(User0),book(Book1).
  evtype(intRmRequest(User0,Book1),libB,inst) :- user(User0),book(Book1).
  evinst(intRmRequest(User0,Book1),libB) :- user(User0),book(Book1).
  ifluent(pow(libB,intRmRequest(User0,Book1)),libB) :- user(User0),book(Book1).
  ifluent(perm(intRmRequest(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(pow(libB,intRmRequest(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(perm(intRmRequest(User0,Book1)),libB) :- user(User0),book(Book1).
  event(viol(intRmRequest(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intRmRequest(User0,Book1)),libB,viol) :- user(User0),book(Book1).
  evinst(viol(intRmRequest(User0,Book1)),libB) :- user(User0),book(Book1).
% Event: intRmBorrow (type: in) of institution libC
  event(intRmBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(intRmBorrow(User0,Book1),libC,inst) :- user(User0),book(Book1).
  evinst(intRmBorrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(pow(libC,intRmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  ifluent(perm(intRmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(pow(libC,intRmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(perm(intRmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  event(viol(intRmBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intRmBorrow(User0,Book1)),libC,viol) :- user(User0),book(Book1).
  evinst(viol(intRmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: intRmBorrow (type: in) of institution libB
  event(intRmBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(intRmBorrow(User0,Book1),libB,inst) :- user(User0),book(Book1).
  evinst(intRmBorrow(User0,Book1),libB) :- user(User0),book(Book1).
  ifluent(pow(libB,intRmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  ifluent(perm(intRmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(pow(libB,intRmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(perm(intRmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  event(viol(intRmBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intRmBorrow(User0,Book1)),libB,viol) :- user(User0),book(Book1).
  evinst(viol(intRmBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
% Event: intBorrow (type: in) of institution libC
  event(intBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(intBorrow(User0,Book1),libC,inst) :- user(User0),book(Book1).
  evinst(intBorrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(pow(libC,intBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  ifluent(perm(intBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(pow(libC,intBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(perm(intBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
  event(viol(intBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intBorrow(User0,Book1)),libC,viol) :- user(User0),book(Book1).
  evinst(viol(intBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: intBorrow (type: in) of institution libB
  event(intBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(intBorrow(User0,Book1),libB,inst) :- user(User0),book(Book1).
  evinst(intBorrow(User0,Book1),libB) :- user(User0),book(Book1).
  ifluent(pow(libB,intBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  ifluent(perm(intBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(pow(libB,intBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  fluent(perm(intBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
  event(viol(intBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intBorrow(User0,Book1)),libB,viol) :- user(User0),book(Book1).
  evinst(viol(intBorrow(User0,Book1)),libB) :- user(User0),book(Book1).
% Event: intBorrow (type: in) of institution pubA
  event(intBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(intBorrow(User0,Book1),pubA,inst) :- user(User0),book(Book1).
  evinst(intBorrow(User0,Book1),pubA) :- user(User0),book(Book1).
  ifluent(pow(pubA,intBorrow(User0,Book1)),pubA) :- user(User0),book(Book1).
  ifluent(perm(intBorrow(User0,Book1)),pubA) :- user(User0),book(Book1).
  fluent(pow(pubA,intBorrow(User0,Book1)),pubA) :- user(User0),book(Book1).
  fluent(perm(intBorrow(User0,Book1)),pubA) :- user(User0),book(Book1).
  event(viol(intBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intBorrow(User0,Book1)),pubA,viol) :- user(User0),book(Book1).
  evinst(viol(intBorrow(User0,Book1)),pubA) :- user(User0),book(Book1).
% Event: intRegister (type: in) of institution libC
  event(intRegister(User0)) :- user(User0).
  evtype(intRegister(User0),libC,inst) :- user(User0).
  evinst(intRegister(User0),libC) :- user(User0).
  ifluent(pow(libC,intRegister(User0)),libC) :- user(User0).
  ifluent(perm(intRegister(User0)),libC) :- user(User0).
  fluent(pow(libC,intRegister(User0)),libC) :- user(User0).
  fluent(perm(intRegister(User0)),libC) :- user(User0).
  event(viol(intRegister(User0))) :- user(User0).
  evtype(viol(intRegister(User0)),libC,viol) :- user(User0).
  evinst(viol(intRegister(User0)),libC) :- user(User0).
% Event: intRegister (type: in) of institution libB
  event(intRegister(User0)) :- user(User0).
  evtype(intRegister(User0),libB,inst) :- user(User0).
  evinst(intRegister(User0),libB) :- user(User0).
  ifluent(pow(libB,intRegister(User0)),libB) :- user(User0).
  ifluent(perm(intRegister(User0)),libB) :- user(User0).
  fluent(pow(libB,intRegister(User0)),libB) :- user(User0).
  fluent(perm(intRegister(User0)),libB) :- user(User0).
  event(viol(intRegister(User0))) :- user(User0).
  evtype(viol(intRegister(User0)),libB,viol) :- user(User0).
  evinst(viol(intRegister(User0)),libB) :- user(User0).
% Event: intRegister (type: in) of institution pubA
  event(intRegister(User0)) :- user(User0).
  evtype(intRegister(User0),pubA,inst) :- user(User0).
  evinst(intRegister(User0),pubA) :- user(User0).
  ifluent(pow(pubA,intRegister(User0)),pubA) :- user(User0).
  ifluent(perm(intRegister(User0)),pubA) :- user(User0).
  fluent(pow(pubA,intRegister(User0)),pubA) :- user(User0).
  fluent(perm(intRegister(User0)),pubA) :- user(User0).
  event(viol(intRegister(User0))) :- user(User0).
  evtype(viol(intRegister(User0)),pubA,viol) :- user(User0).
  evinst(viol(intRegister(User0)),pubA) :- user(User0).
%
% Violation events of institution {inst}
%
% Event: issueFine (type: in)
  event(issueFine(User0,Book1)) :- user(User0),book(Book1).
  evtype(issueFine(User0,Book1),libC,viol) :- user(User0),book(Book1).
  evinst(issueFine(User0,Book1),libC) :- user(User0),book(Book1).
% Event: issueFine (type: in)
  event(issueFine(User0,Book1)) :- user(User0),book(Book1).
  evtype(issueFine(User0,Book1),libB,viol) :- user(User0),book(Book1).
  evinst(issueFine(User0,Book1),libB) :- user(User0),book(Book1).
% Event: issueFine (type: in)
  event(issueFine(User0,Book1)) :- user(User0),book(Book1).
  evtype(issueFine(User0,Book1),pubA,viol) :- user(User0),book(Book1).
  evinst(issueFine(User0,Book1),pubA) :- user(User0),book(Book1).
%
% Creation events
%
%
% Dissolution events
%
%
% dissolve events
%
%
% inertial fluents 
%
ifluent(inDebt(User0,Book1),libC) :-
  user(User0),book(Book1).
fluent(inDebt(User0,Book1),libC) :-
  user(User0),book(Book1).

ifluent(inDebt(User0,Book1),libB) :-
  user(User0),book(Book1).
fluent(inDebt(User0,Book1),libB) :-
  user(User0),book(Book1).

ifluent(inDebt(User0,Book1),pubA) :-
  user(User0),book(Book1).
fluent(inDebt(User0,Book1),pubA) :-
  user(User0),book(Book1).

%
% noninertial fluents
%
%
% violation fluents (to be implemented)

%
% obligation fluents
%
%
% cross fluents
%
fluent(gpow(I0,rmBorrow(User0,Book1),I1), bridge) :- 
    inst(I0; I1; bridge), 
    event(rmBorrow(User0,Book1)), evinst(rmBorrow(User0,Book1), I1), evtype(rmBorrow(User0,Book1), I1, ex), user(User0),book(Book1).
ifluent(gpow(I0,rmBorrow(User0,Book1),I1), bridge) :- 
    inst(I0; I1; bridge), 
    event(rmBorrow(User0,Book1)), evinst(rmBorrow(User0,Book1), I1), evtype(rmBorrow(User0,Book1), I1, ex), user(User0),book(Book1).
fluent(gpow(I0,rmRegister(User0),I1), bridge) :- 
    inst(I0; I1; bridge), 
    event(rmRegister(User0)), evinst(rmRegister(User0), I1), evtype(rmRegister(User0), I1, ex), user(User0).
ifluent(gpow(I0,rmRegister(User0),I1), bridge) :- 
    inst(I0; I1; bridge), 
    event(rmRegister(User0)), evinst(rmRegister(User0), I1), evtype(rmRegister(User0), I1, ex), user(User0).
fluent(ipow(I0,inDebt(User,Book),I1), bridge) :- 
    inst(I0; I1; bridge), 
   book(Book),
   user(User),
    fluent(inDebt(User,Book), I1).
ifluent(ipow(I0,inDebt(User,Book),I1), bridge) :- 
    inst(I0; I1; bridge), 
   book(Book),
   user(User),
    fluent(inDebt(User,Book), I1).
%
% -------------------------------PART 2-------------------------------
%
%
% cross generate rules
%
%
% Translation of intRmRequest(User,Book) of libC xgenerates rmBorrow(User,Book) of libB if [] in 
occurred(rmBorrow(User,Book),libB,I) :- occurred(intRmRequest(User,Book),libC,I),
   holdsat(gpow(libC,rmBorrow(User,Book),libB),bridge,I), 
   inst(libB;libC), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of intRmRequest(User,Book) of libB xgenerates rmBorrow(User,Book) of libC if [] in 
occurred(rmBorrow(User,Book),libC,I) :- occurred(intRmRequest(User,Book),libB,I),
   holdsat(gpow(libB,rmBorrow(User,Book),libC),bridge,I), 
   inst(libC;libB), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of intRegister(User) of libC xgenerates rmRegister(User) of libB if [] in 
occurred(rmRegister(User),libB,I) :- occurred(intRegister(User),libC,I),
   holdsat(gpow(libC,rmRegister(User),libB),bridge,I), 
   inst(libB;libC), 
   user(User),
   inst(bridge), instant(I).
%
% Translation of intRegister(User) of libB xgenerates rmRegister(User) of libC if [] in 
occurred(rmRegister(User),libC,I) :- occurred(intRegister(User),libB,I),
   holdsat(gpow(libB,rmRegister(User),libC),bridge,I), 
   inst(libC;libB), 
   user(User),
   inst(bridge), instant(I).
%
% Translation of intRegister(User) of pubA xgenerates rmRegister(User) of libC if [] in 
occurred(rmRegister(User),libC,I) :- occurred(intRegister(User),pubA,I),
   holdsat(gpow(pubA,rmRegister(User),libC),bridge,I), 
   inst(libC;pubA), 
   user(User),
   inst(bridge), instant(I).
%
% Translation of intRegister(User) of pubA xgenerates rmRegister(User) of libB if [] in 
occurred(rmRegister(User),libB,I) :- occurred(intRegister(User),pubA,I),
   holdsat(gpow(pubA,rmRegister(User),libB),bridge,I), 
   inst(libB;pubA), 
   user(User),
   inst(bridge), instant(I).
%
% cross initiation rules
%
%
% Translation of issueFine(User,Book) of libC xinitiates ['inDebt', ['User', 'Book']] of libB if []
%
xinitiated(libC, inDebt(User,Book),libB,I) :-
   occurred(issueFine(User,Book),libC,I),
   holdsat(ipow(libC, inDebt(User,Book), libB), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(libB;libC), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of issueFine(User,Book) of libC xinitiates ['inDebt', ['User', 'Book']] of pubA if []
%
xinitiated(libC, inDebt(User,Book),pubA,I) :-
   occurred(issueFine(User,Book),libC,I),
   holdsat(ipow(libC, inDebt(User,Book), pubA), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(pubA;libC), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of issueFine(User,Book) of libB xinitiates ['inDebt', ['User', 'Book']] of libC if []
%
xinitiated(libB, inDebt(User,Book),libC,I) :-
   occurred(issueFine(User,Book),libB,I),
   holdsat(ipow(libB, inDebt(User,Book), libC), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(libC;libB), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of issueFine(User,Book) of libB xinitiates ['inDebt', ['User', 'Book']] of pubA if []
%
xinitiated(libB, inDebt(User,Book),pubA,I) :-
   occurred(issueFine(User,Book),libB,I),
   holdsat(ipow(libB, inDebt(User,Book), pubA), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(pubA;libB), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of issueFine(User,Book) of pubA xinitiates ['inDebt', ['User', 'Book']] of libC if []
%
xinitiated(pubA, inDebt(User,Book),libC,I) :-
   occurred(issueFine(User,Book),pubA,I),
   holdsat(ipow(pubA, inDebt(User,Book), libC), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(libC;pubA), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% Translation of issueFine(User,Book) of pubA xinitiates ['inDebt', ['User', 'Book']] of libB if []
%
xinitiated(pubA, inDebt(User,Book),libB,I) :-
   occurred(issueFine(User,Book),pubA,I),
   holdsat(ipow(pubA, inDebt(User,Book), libB), bridge, I), 
   holdsat(live(bridge),bridge,I), inst(bridge), 
   inst(libB;pubA), 
   book(Book),
   user(User),
   inst(bridge), instant(I).
%
% cross termination rules
%
%
% -------------------------------PART 3-------------------------------
%
%
% initially
%
% no creation event
holdsat(live(bridge),bridge,I) :- start(I), inst(bridge).
holdsat(perm(null),bridge,I) :- start(I), inst(bridge).
% initially: gpow(libB,rmRegister(User),libC)
holdsat(gpow(libB,rmRegister(User),libC),bridge,I) :-
   user(User),
   inst(libC; libB), 
   inst(bridge), start(I).
% initially: gpow(libC,rmRegister(User),libB)
holdsat(gpow(libC,rmRegister(User),libB),bridge,I) :-
   user(User),
   inst(libB; libC), 
   inst(bridge), start(I).
% initially: gpow(libB,rmBorrow(User,Book),libC)
holdsat(gpow(libB,rmBorrow(User,Book),libC),bridge,I) :-
   book(Book),
   user(User),
   inst(libC; libB), 
   inst(bridge), start(I).
% initially: gpow(libC,rmBorrow(User,Book),libB)
holdsat(gpow(libC,rmBorrow(User,Book),libB),bridge,I) :-
   book(Book),
   user(User),
   inst(libB; libC), 
   inst(bridge), start(I).
% initially: ipow(libB,inDebt(User,Book),libC)
holdsat(ipow(libB,inDebt(User,Book),libC),bridge,I) :-
   book(Book),
   user(User),
   inst(libC; libB), 
   inst(bridge), start(I).
% initially: ipow(libC,inDebt(User,Book),libB)
holdsat(ipow(libC,inDebt(User,Book),libB),bridge,I) :-
   book(Book),
   user(User),
   inst(libB; libC), 
   inst(bridge), start(I).
%
% End of file
%
