compObserved(shareRequest(bob, bob_data, nsa),0).
compObserved(null,1).
compObserved(approveRequest(bob, bob_data, nsa),2).
compObserved(approveRequest(alice, alice_data, nsa),3).
compObserved(approve(alice, alice_data, nsa),4).
compObserved(share(bob,bob_data,nsa), 5).
compObserved(share(alice,alice_data,nsa), 6).


#hide. 
#show observed(A,B,C).




