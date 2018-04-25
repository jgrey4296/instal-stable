%
% Domain declarations for libC
%
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
% Standard prelude for libC
%
% instant ordering
% removed for MDV 20130117
%%% before(I1,I2):- next(I1,I2),instant(I1), instant(I2).
%%% before(I1,I3):- before(I1,I2),before(I2,I3),
%%%    instant(I1),instant(I2),instant(I3).
% fluent rules
holdsat(P,In,J):- holdsat(P,In,I),not terminated(P,In,I),
    next(I,J),ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
    ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J), 
    oblfluent(P, In),instant(I),instant(J), inst(In).
% all observed events occur
occurred(E,In,I):- evtype(E,In,ex),observed(E,In,I),instant(I), inst(In).
% produces null for unknown events 
occurred(null,In,I) :- not evtype(E,In,ex), observed(E,In,I), 
    instant(I), inst(In). 
% produces gap warning for unknown events 
unknown(E, In, I) :- not evtype(E,In,ex), observed(E,In,I), 
    instant(I), inst(In). 
warninggap(In, I) :- unknown(E,In,I), inst(In), instant(I). 
% a violation occurs for each non-permitted action 
occurred(viol(E),In,I):-
    occurred(E,In,I),
    evtype(E,In,ex),
    not holdsat(perm(E),In,I),
    holdsat(live(In),In,I),evinst(E,In),
    event(E),instant(I),event(viol(E)),inst(In).
occurred(viol(E),In,I):-
    occurred(E,In,I),
    evtype(E,In,inst),
    not holdsat(perm(E),In,I),
    event(E),instant(I),event(viol(E)), inst(In).
% needed until I tidy up some of the constraint generation 
true.
%
% Rules for Institution libC
%
  ifluent(live(libC), libC).
  fluent(live(libC), libC).
  inst(libC).
%
% Constraints for obserable events depending on mode option
%
%%  mode COMPOSITE is chosen:
{compObserved(E, J)}:- evtype(E,In,ex),instant(J), not final(J), inst(In).
:- compObserved(E,J),compObserved(F,J),instant(J),evtype(E,InX,ex),
   evtype(F,InY,ex), E!=F,inst(InX;InY). 
obs(I):- compObserved(E,I),evtype(E,In,ex),instant(I),inst(In).
      :- not obs(I), not final(I), instant(I), inst(In).
observed(E,In,I) :- compObserved(E,I), inst(In), instant(I).
%
% The following types were declared:
%
% Book
% User
% Number
%
% Exogenous events
% Event: rmBorrow (type: ex)
  event(rmBorrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(rmBorrow(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(rmBorrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(rmBorrow(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(rmBorrow(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(rmBorrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(rmBorrow(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(rmBorrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: register (type: ex)
  event(register(User0)) :- user(User0).
  evtype(register(User0),libC,ex) :- user(User0).
  evinst(register(User0),libC) :- user(User0).
  ifluent(perm(register(User0)), libC) :- user(User0).
  fluent(perm(register(User0)), libC) :- user(User0).
  event(viol(register(User0))) :- user(User0).
  evtype(viol(register(User0)), libC, viol) :- user(User0).
  evinst(viol(register(User0)),libC) :- user(User0).
% Event: borrow (type: ex)
  event(borrow(User0,Book1)) :- user(User0),book(Book1).
  evtype(borrow(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(borrow(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(borrow(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(borrow(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(borrow(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(borrow(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(borrow(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: return (type: ex)
  event(return(User0,Book1)) :- user(User0),book(Book1).
  evtype(return(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(return(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(return(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(return(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(return(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(return(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(return(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: rmRequest (type: ex)
  event(rmRequest(User0,Book1)) :- user(User0),book(Book1).
  evtype(rmRequest(User0,Book1),libC,ex) :- user(User0),book(Book1).
  evinst(rmRequest(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(perm(rmRequest(User0,Book1)), libC) :- user(User0),book(Book1).
  fluent(perm(rmRequest(User0,Book1)), libC) :- user(User0),book(Book1).
  event(viol(rmRequest(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(rmRequest(User0,Book1)), libC, viol) :- user(User0),book(Book1).
  evinst(viol(rmRequest(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: rmRegister (type: ex)
  event(rmRegister(User0)) :- user(User0).
  evtype(rmRegister(User0),libC,ex) :- user(User0).
  evinst(rmRegister(User0),libC) :- user(User0).
  ifluent(perm(rmRegister(User0)), libC) :- user(User0).
  fluent(perm(rmRegister(User0)), libC) :- user(User0).
  event(viol(rmRegister(User0))) :- user(User0).
  evtype(viol(rmRegister(User0)), libC, viol) :- user(User0).
  evinst(viol(rmRegister(User0)),libC) :- user(User0).
%
% null event for unknown events
% Event: null (type: ex)
  event(null).
  evtype(null,libC,ex).
  evinst(null,libC).
  ifluent(perm(null), libC).
  fluent(perm(null), libC).
  event(viol(null)).
  evtype(viol(null),libC,viol).
  evinst(viol(null),libC).
% Institutional events
% Event: intReturn (type: in)
  event(intReturn(User0,Book1)) :- user(User0),book(Book1).
  evtype(intReturn(User0,Book1),libC,inst) :- user(User0),book(Book1).
  evinst(intReturn(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(pow(libC,intReturn(User0,Book1)),libC) :- user(User0),book(Book1).
  ifluent(perm(intReturn(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(pow(libC,intReturn(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(perm(intReturn(User0,Book1)),libC) :- user(User0),book(Book1).
  event(viol(intReturn(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(intReturn(User0,Book1)),libC,viol) :- user(User0),book(Book1).
  evinst(viol(intReturn(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: intRmRegister (type: in)
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
% Event: intRmBorrow (type: in)
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
% Event: due (type: in)
  event(due(User0,Book1)) :- user(User0),book(Book1).
  evtype(due(User0,Book1),libC,inst) :- user(User0),book(Book1).
  evinst(due(User0,Book1),libC) :- user(User0),book(Book1).
  ifluent(pow(libC,due(User0,Book1)),libC) :- user(User0),book(Book1).
  ifluent(perm(due(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(pow(libC,due(User0,Book1)),libC) :- user(User0),book(Book1).
  fluent(perm(due(User0,Book1)),libC) :- user(User0),book(Book1).
  event(viol(due(User0,Book1))) :- user(User0),book(Book1).
  evtype(viol(due(User0,Book1)),libC,viol) :- user(User0),book(Book1).
  evinst(viol(due(User0,Book1)),libC) :- user(User0),book(Book1).
% Event: intRegister (type: in)
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
% Event: intBorrow (type: in)
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
% Event: intRmRequest (type: in)
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
%
% Violation events
%
% Event: issueFine (type: in)
  event(issueFine(User0,Book1)) :- user(User0),book(Book1).
  evtype(issueFine(User0,Book1),libC,viol) :- user(User0),book(Book1).
  evinst(issueFine(User0,Book1),libC) :- user(User0),book(Book1).
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
ifluent(borrowed(User0,Book1),libC) :-
  user(User0),book(Book1).
fluent(borrowed(User0,Book1),libC) :-
  user(User0),book(Book1).

ifluent(inDebt(User0,Book1),libC) :-
  user(User0),book(Book1).
fluent(inDebt(User0,Book1),libC) :-
  user(User0),book(Book1).

ifluent(inCollection(Book0),libC) :-
  book(Book0).
fluent(inCollection(Book0),libC) :-
  book(Book0).

ifluent(onLoan(Book0),libC) :-
  book(Book0).
fluent(onLoan(Book0),libC) :-
  book(Book0).

ifluent(next(Number0,Number1),libC) :-
  number(Number0),number(Number1).
fluent(next(Number0,Number1),libC) :-
  number(Number0),number(Number1).

ifluent(member(User0),libC) :-
  user(User0).
fluent(member(User0),libC) :-
  user(User0).

ifluent(allowance(User0,Number1),libC) :-
  user(User0),number(Number1).
fluent(allowance(User0,Number1),libC) :-
  user(User0),number(Number1).

ifluent(loans(User0,Number1),libC) :-
  user(User0),number(Number1).
fluent(loans(User0,Number1),libC) :-
  user(User0),number(Number1).

ifluent(registeredUser(User0),libC) :-
  user(User0).
fluent(registeredUser(User0),libC) :-
  user(User0).

%
% noninertial fluents
%
nifluent(available(Book0), libC) :-
  book(Book0).
fluent(available(Book0), libC) :-
  book(Book0).

nifluent(normalUser(User0), libC) :-
  user(User0).
fluent(normalUser(User0), libC) :-
  user(User0).

%
% violation fluents (to be implemented)

%
% obligation fluents
%
oblfluent(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)), libC) :-
   event(intReturn(User0,Book1)),
   event(due(User2,Book3)),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
ifluent(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)), libC) :-
   event(intReturn(User0,Book1)),
   event(due(User2,Book3)),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
fluent(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)), libC) :-
   event(intReturn(User0,Book1)),
   event(due(User2,Book3)),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
terminated(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)),libC,I) :-
   event(intReturn(User0,Book1)), occurred(intReturn(User0,Book1),libC,I),
   event(due(User2,Book3)),
   holdsat(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)),libC,I),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
terminated(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)),libC,I) :-
   event(intReturn(User0,Book1)), 
   event(due(User2,Book3)), occurred(due(User2,Book3),libC,I),
   holdsat(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)),libC,I),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
occurred(issueFine(User4,Book5),libC,I) :-
   event(intReturn(User0,Book1)), 
   event(due(User2,Book3)), occurred(due(User2,Book3),libC,I),
   holdsat(obl(intReturn(User0,Book1),due(User2,Book3),issueFine(User4,Book5)),libC,I),
   event(issueFine(User4,Book5)), user(User0),book(Book1),user(User2),book(Book3),user(User4),book(Book5),inst(libC).
%
% -------------------------------PART 2-------------------------------
%
%
% generate rules
%
%
% Translation of intBorrow(User,Book) generates due(User,Book) if ['and', ['normalUser', ['User']], ['available', ['Book']]] in +3
occurred(due(User,Book),libC,I+3) :- occurred(intBorrow(User,Book),libC,I),
   holdsat(pow(libC,due(User,Book)),libC,I+3),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of return(User,Book) generates intReturn(User,Book) if ['registeredUser', ['User']] in 
occurred(intReturn(User,Book),libC,I) :- occurred(return(User,Book),libC,I),
   holdsat(pow(libC,intReturn(User,Book)),libC,I),
   holdsat(registeredUser(User),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of rmBorrow(User,Book) generates intBorrow(User,Book) if ['and', ['registeredUser', ['User']], ['not', ['member', ['User']]]] in 
occurred(intBorrow(User,Book),libC,I) :- occurred(rmBorrow(User,Book),libC,I),
   holdsat(pow(libC,intBorrow(User,Book)),libC,I),
   holdsat(registeredUser(User),libC,I),
   not
   holdsat(member(User),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of rmRequest(User,Book) generates intRmRequest(User,Book) if ['and', ['member', ['User']], ['not', ['available', ['Book']]]] in 
occurred(intRmRequest(User,Book),libC,I) :- occurred(rmRequest(User,Book),libC,I),
   holdsat(pow(libC,intRmRequest(User,Book)),libC,I),
   holdsat(member(User),libC,I),
   not
   holdsat(available(Book),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of borrow(User,Book) generates intBorrow(User,Book) if ['member', ['User']] in 
occurred(intBorrow(User,Book),libC,I) :- occurred(borrow(User,Book),libC,I),
   holdsat(pow(libC,intBorrow(User,Book)),libC,I),
   holdsat(member(User),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of rmRegister(User) generates intRmRegister(User) if [] in 
occurred(intRmRegister(User),libC,I) :- occurred(rmRegister(User),libC,I),
   holdsat(pow(libC,intRmRegister(User)),libC,I),
   user(User),
   inst(libC), instant(I).
%
% Translation of register(User) generates intRegister(User) if ['member', ['User']] in 
occurred(intRegister(User),libC,I) :- occurred(register(User),libC,I),
   holdsat(pow(libC,intRegister(User)),libC,I),
   holdsat(member(User),libC,I),
   user(User),
   inst(libC), instant(I).
%
% initiate rules
%
%
% Translation of issueFine(User,Book) initiates ['inDebt', ['User', 'Book']] if []
%
initiated(inDebt(User,Book),libC,I) :-
   occurred(issueFine(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of intReturn(User,Book) initiates ['loans', ['User', 'NewNumber']] if ['and', ['loans', ['User', 'Number']], ['next', ['NewNumber', 'Number']]]
%
initiated(loans(User,NewNumber),libC,I) :-
   occurred(intReturn(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(loans(User,Number),libC,I),
   holdsat(next(NewNumber,Number),libC,I),
   number(NewNumber),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['perm', ['return', ['User', 'Book']]] if ['and', ['normalUser', ['User']], ['available', ['Book']]]
%
initiated(perm(return(User,Book)),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['perm', ['intReturn', ['User', 'Book']]] if ['and', ['normalUser', ['User']], ['available', ['Book']]]
%
initiated(perm(intReturn(User,Book)),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['pow', ['intReturn', ['User', 'Book']]] if ['and', ['normalUser', ['User']], ['available', ['Book']]]
%
initiated(pow(libC,intReturn(User,Book)),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   book(Book),
   user(User),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['borrowed', ['User', 'Book']] if ['and', ['and', ['and', ['normalUser', ['User']], ['available', ['Book']]], ['loans', ['User', 'Number']]], ['next', ['Number', 'NewNumber']]]
%
initiated(borrowed(User,Book),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   holdsat(loans(User,Number),libC,I),
   holdsat(next(Number,NewNumber),libC,I),
   number(NewNumber),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['onLoan', ['Book']] if ['and', ['and', ['and', ['normalUser', ['User']], ['available', ['Book']]], ['loans', ['User', 'Number']]], ['next', ['Number', 'NewNumber']]]
%
initiated(onLoan(Book),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   holdsat(loans(User,Number),libC,I),
   holdsat(next(Number,NewNumber),libC,I),
   number(NewNumber),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['loans', ['User', 'NewNumber']] if ['and', ['and', ['and', ['normalUser', ['User']], ['available', ['Book']]], ['loans', ['User', 'Number']]], ['next', ['Number', 'NewNumber']]]
%
initiated(loans(User,NewNumber),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   holdsat(loans(User,Number),libC,I),
   holdsat(next(Number,NewNumber),libC,I),
   number(NewNumber),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) initiates ['obl', [['intReturn', ['User', 'Book']], ['due', ['User', 'Book']], ['issueFine', ['User', 'Book']]]] if ['and', ['and', ['and', ['normalUser', ['User']], ['available', ['Book']]], ['loans', ['User', 'Number']]], ['next', ['Number', 'NewNumber']]]
%
initiated(obl(intReturn(User,Book),due(User,Book),issueFine(User,Book)),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   holdsat(loans(User,Number),libC,I),
   holdsat(next(Number,NewNumber),libC,I),
   number(NewNumber),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['perm', ['rmBorrow', ['User', 'Book']]] if []
%
initiated(perm(rmBorrow(User,Book)),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['perm', ['intBorrow', ['User', 'Book']]] if []
%
initiated(perm(intBorrow(User,Book)),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['pow', ['intBorrow', ['User', 'Book']]] if []
%
initiated(pow(libC,intBorrow(User,Book)),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['registeredUser', ['User']] if []
%
initiated(registeredUser(User),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['allowance', ['User', '1']] if []
%
initiated(allowance(User,1),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% Translation of intRmRegister(User) initiates ['loans', ['User', '0']] if []
%
initiated(loans(User,0),libC,I) :-
   occurred(intRmRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['perm', ['rmRequest', ['User', 'Book']]] if []
%
initiated(perm(rmRequest(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['perm', ['intRmRequest', ['User', 'Book']]] if []
%
initiated(perm(intRmRequest(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['pow', ['intRmRequest', ['User', 'Book']]] if []
%
initiated(pow(libC,intRmRequest(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['perm', ['borrow', ['User', 'Book']]] if []
%
initiated(perm(borrow(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['perm', ['intBorrow', ['User', 'Book']]] if []
%
initiated(perm(intBorrow(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['pow', ['intBorrow', ['User', 'Book']]] if []
%
initiated(pow(libC,intBorrow(User,Book)),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   book(Book),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['registeredUser', ['User']] if []
%
initiated(registeredUser(User),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['allowance', ['User', '2']] if []
%
initiated(allowance(User,2),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% Translation of intRegister(User) initiates ['loans', ['User', '0']] if []
%
initiated(loans(User,0),libC,I) :-
   occurred(intRegister(User),libC,I),
   holdsat(live(libC),libC,I), inst(libC),
   user(User),
   inst(libC), instant(I).
%
% terminate rules
%
%
% Translation of intReturn(User,Book) terminates ['onLoan', ['Book']] if ['loans', ['User', 'Number']]
%
terminated(onLoan(Book),libC,I) :-
   occurred(intReturn(User,Book),libC,I),
   holdsat(live(libC),libC,I),inst(libC),
   holdsat(loans(User,Number),libC,I),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intReturn(User,Book) terminates ['borrowed', ['User', 'Book']] if ['loans', ['User', 'Number']]
%
terminated(borrowed(User,Book),libC,I) :-
   occurred(intReturn(User,Book),libC,I),
   holdsat(live(libC),libC,I),inst(libC),
   holdsat(loans(User,Number),libC,I),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intReturn(User,Book) terminates ['loans', ['User', 'Number']] if ['loans', ['User', 'Number']]
%
terminated(loans(User,Number),libC,I) :-
   occurred(intReturn(User,Book),libC,I),
   holdsat(live(libC),libC,I),inst(libC),
   holdsat(loans(User,Number),libC,I),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% Translation of intBorrow(User,Book) terminates ['loans', ['User', 'Number']] if ['and', ['and', ['normalUser', ['User']], ['available', ['Book']]], ['loans', ['User', 'Number']]]
%
terminated(loans(User,Number),libC,I) :-
   occurred(intBorrow(User,Book),libC,I),
   holdsat(live(libC),libC,I),inst(libC),
   holdsat(normalUser(User),libC,I),
   holdsat(available(Book),libC,I),
   holdsat(loans(User,Number),libC,I),
   book(Book),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% noninertial rules
%
%
% Translation of available(Book) when ['and', ['inCollection', ['Book']], ['not', ['onLoan', ['Book']]]]
holdsat(available(Book),libC,I) :-
   holdsat(inCollection(Book),libC,I),
   not
   holdsat(onLoan(Book),libC,I),
   book(Book),
   inst(libC), instant(I).
%
% Translation of normalUser(User) when ['and', ['and', ['and', ['registeredUser', ['User']], ['allowance', ['User', 'Max']]], ['loans', ['User', 'Number']]], ['<', ['Number', 'Max']]]
holdsat(normalUser(User),libC,I) :-
   holdsat(registeredUser(User),libC,I),
   holdsat(allowance(User,Max),libC,I),
   holdsat(loans(User,Number),libC,I),
   Number<Max,
   number(Max),
   user(User),
   number(Number),
   inst(libC), instant(I).
%
% -------------------------------PART 3-------------------------------
%
%
% initially
%
% no creation event
holdsat(live(libC),libC,I) :- start(I), inst(libC).
holdsat(perm(null),libC,I) :- start(I), inst(libC).
% initially: perm(register(User))
holdsat(perm(register(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: perm(intRegister(User))
holdsat(perm(intRegister(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: pow(libC,intRegister(User))
holdsat(pow(libC,intRegister(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: perm(due(User,Book))
holdsat(perm(due(User,Book)),libC,I) :-
   book(Book),
   user(User),
   inst(libC), start(I).
% initially: pow(libC,due(User,Book))
holdsat(pow(libC,due(User,Book)),libC,I) :-
   book(Book),
   user(User),
   inst(libC), start(I).
% initially: next(0,1)
holdsat(next(0,1),libC,I) :-
   inst(libC), start(I).
% initially: next(1,2)
holdsat(next(1,2),libC,I) :-
   inst(libC), start(I).
% initially: next(2,3)
holdsat(next(2,3),libC,I) :-
   inst(libC), start(I).
% initially: next(3,4)
holdsat(next(3,4),libC,I) :-
   inst(libC), start(I).
% initially: next(4,5)
holdsat(next(4,5),libC,I) :-
   inst(libC), start(I).
% initially: perm(rmRegister(User))
holdsat(perm(rmRegister(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: perm(intRmRegister(User))
holdsat(perm(intRmRegister(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: pow(libC,intRmRegister(User))
holdsat(pow(libC,intRmRegister(User)),libC,I) :-
   user(User),
   inst(libC), start(I).
% initially: perm(rmBorrow(User,Book))
holdsat(perm(rmBorrow(User,Book)),libC,I) :-
   book(Book),
   user(User),
   inst(libC), start(I).
% initially: inCollection(book1_c)
holdsat(inCollection(book1_c),libC,I) :-
   inst(libC), start(I).
% initially: inCollection(book2_c)
holdsat(inCollection(book2_c),libC,I) :-
   inst(libC), start(I).
% initially: member(alice)
holdsat(member(alice),libC,I) :-
   inst(libC), start(I).
%
% End of file
%
