%% Translation of {inev} initiates {inits} if {condition}
%%
initiated({inf},{inst},I) :-
  occurred({ev},{inst},I),
  not occurred(viol({ev}),{inst},I),
  holdsat(live({inst}),{inst},I),
  inst({inst}),
