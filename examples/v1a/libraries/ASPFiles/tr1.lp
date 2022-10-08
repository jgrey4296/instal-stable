%%% test trace tr1 for pubA only 


observed(register(bob),pubA, 0).
observed(register(alice),pubA,1).
observed(borrow(bob, book1_a),pubA, 2).
observed(borrow(alice, book1_a), pubA,3).  % borrow a book on loan
observed(borrow(bob, book2_a), pubA,4).
observed(borrow(bob, book3_a), pubA,5).
observed(borrow(bob, book4_a), pubA,6).  % borrow more than allowance
observed(return(bob, book3_a), pubA,7).  % return in time 
observed(borrow(alice, book1_b), pubA,8). % borrow a book not in collection


#hide. 
%#show holdsat(allowance(A, B), C, I). 
%#show holdsat(available(b1), C, I).
%#show holdsat(normalUser(bob), C, I). 

#show holdsat(inDebt(A, Book), C, I). 
#show holdsat(loans(A, Book), C, I). 
#show holdsat(borrowed(B, A), C, I). 
#show occurred(A,pubA,I).

%#show holdsat(obl(intReturn(bob, b3_a),B,C),pubA,I).
%#show occurred(intBorrow(User, Book), pubA, I). 
