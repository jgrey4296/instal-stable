%%% test trace ctr1 for coordinated institution 
compObserved(register(bob), 0).   % only pubA and libB response 
compObserved(register(alice), 1).  % only pubA and libC response 

compObserved(extend(alice), 2).  % only pubA recognises 

compObserved(borrow(bob, book1_a), 3).  % succeed
compObserved(borrow(alice, book1_a), 4).  % borrow a book on loan

compObserved(borrow(bob, book2_a), 5). % succeed
compObserved(borrow(bob, book3_a), 6). % borrow more than allowance; due to return book1_a;
compObserved(return(bob, book2_a), 7).  % book2_a return in time ;
compObserved(borrow(alice, book1_b), 8). % borrow from external lib. 

compObserved(borrow(alice, book2_a), 9). % succeed, borrow a book just returned 
compObserved(borrow(alice, book1_c), 10). % succeed, borrow a book from libC


#hide. 

#show occurred(A, In, I).

#show holdsat(available(A), In, I). 
#show holdsat(normalUser(A), In, I). 
#show holdsat(allowance(A, B), In, I). 
#show holdsat(loans(A, B), In, I). 
#show holdsat(inDebt(A, B), In, I). 
#show holdsat(borrowed(A, B), In, I). 
#show holdsat(member(A), In, I).




#show initiated(available(A), In, I). 
#show initiated(normalUser(A), In, I). 
#show initiated(allowance(A, B), In, I). 
#show initiated(loans(A, B), In, I). 
#show initiated(inDebt(A, B), In, I). 
#show initiated(borrowed(A, B), In, I). 


#show terminated(available(A), In, I). 
#show terminated(normalUser(A), In, I). 
#show terminated(allowance(A, B), In, I). 
#show terminated(loans(A, B), In, I). 
#show terminated(inDebt(A, B), In, I). 
#show terminated(borrowed(A, B), In, I). 


