%%% test trace tr2 for libB only 

observed(register(bob),libB, 0).
observed(register(alice),libB,1).     % ext users cannot use register 
observed(extRegister(alice),libB,2).   % ext users can only use extRegister
observed(borrow(alice, book1_b), libB,3).   % ext users cannot use borrow 
observed(extBorrow(alice, book1_b), libB,4).  % ext users can only use extBorrow
observed(extBorrow(alice, book1_b), libB,5).  % ext users can only borrow one 
observed(return(alice, book1_b), libB,6). % success 
observed(borrow(bob, book1_b), libB,7).  % the book is on loan
observed(borrow(bob, book2_b), libB,8). % success 


#hide. 
%#show holdsat(allowance(A, B), C, I). 
%#show holdsat(available(b1), C, I).
%#show holdsat(normalUser(bob), C, I). 

#show holdsat(inDebt(A, Book), C, I). 
%#show holdsat(borrowed(B, A), C, I). 
#show occurred(A,B,6).

%#show holdsat(obl(return(bob,b2),due(User2,Book3),issueFine(User4,Book5)),pubA,I).
%#show occurred(intBorrow(User, Book), pubA, I). 
