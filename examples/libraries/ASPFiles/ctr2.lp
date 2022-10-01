%%% test trace ctr2 for interacting institution 
compObserved(register(bob), 0).   % only pubA and libB response 
compObserved(register(alice), 1).  % only pubA and libC response 

compObserved(borrow(bob, book1_a), 2).  % succeed
compObserved(rmRequest(bob, book1_c), 3).  % gens ex_borrow for libC, succeed, 
compObserved(rmRequest(bob, book2_c), 4).  % gens ex_borrow for libC, failed; one item only.   

compObserved(borrow(alice, book1_c), 5).  % borrow a book on loan; due to return book1_a. 
compObserved(borrow(alice, book2_c), 6).  % succeed; due to return book1_c. 

compObserved(return(alice, book2_c), 7).  % succeed; return in time.  

compObserved(extend(alice), 8).  % only pubA offers allowance extension. 

#hide. 


#show occurred(A, In, I).

#show holdsat(available(A), In, I). 
#show holdsat(normalUser(A), In, I). 
#show holdsat(allowance(A, B), In, I). 
#show holdsat(loans(A, B), In, I). 
#show holdsat(inDebt(A, B), In, I). 
#show holdsat(borrowed(A, B), In, I). 
%#show holdsat(gpow(libB, rmRegister(bob), libC), bridge, I). 
%#show holdsat(gpow(libC, rmRegister(alice), libB), bridge, I). 
%#show holdsat(gpow(libB, rmBorrow(bob, book1_c), libC), bridge, I). 
%#show holdsat(gpow(libB, rmBorrow(bob, book2_c), libC), bridge, I). 
%#show holdsat(ipow(libC, inDebt(bob, book1_c), libB), In, I). 


#show initiated(available(A), In, I). 
#show initiated(normalUser(A), In, I). 
#show initiated(allowance(A, B), In, I). 
#show initiated(loans(A, B), In, I). 
#show initiated(inDebt(A, B), In, I). 
#show initiated(borrowed(A, B), In, I). 
%#show initiated(gpow(libB, rmRegister(bob), libC), bridge, I). 
%#show initiated(gpow(libC, rmRegister(alice), libB), bridge, I). 
%#show initiated(gpow(libB, rmBorrow(bob, book1_c), libC), bridge, I). 
%#show initiated(gpow(libB, rmBorrow(bob, book2_c), libC), bridge, I). 
%#show holdsat(ipow(libC, inDebt(bob, book1_c), libB), In, I). 

#show terminated(available(A), In, I). 
#show terminated(normalUser(A), In, I). 
#show terminated(allowance(A, B), In, I). 
#show terminated(loans(A, B), In, I). 
#show terminated(inDebt(A, B), In, I). 
#show terminated(borrowed(A, B), In, I). 
%#show terminated(gpow(libB, rmRegister(bob), libC), bridge, I). 
%#show terminated(gpow(libC, rmRegister(alice), libB), bridge, I). 
%#show terminated(gpow(libB, rmBorrow(bob, book1_c), libC), bridge, I). 
%#show terminated(gpow(libB, rmBorrow(bob, book2_c), libC), bridge, I). 
%#show terminated(ipow(libC, inDebt(bob, book1_c), libB), In, I). 



%#show holdsat(allowance(A, Number), pubA, 8..9).
%#show holdsat(loans(alice, Number), I, 8). 

%#show holdsat(borrowed(alice, Book), I, 8). 


%#show holdsat(inDebt(A, B), I, 5..7). 

%#show holdsat(normalUser(bob), libB, I). 
%#show holdsat(registeredUser(bob), libC, 4). 

%% To do:
% try extend of pubA 
