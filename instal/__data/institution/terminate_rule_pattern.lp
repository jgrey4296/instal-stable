%% Translation of {inev} terminates {terms} if {condition}
terminated({inf},{inst},I) :-
  occurred({ev},{inst},I),
  not occurred(viol({ev}),{inst},I),
  holdsat(live({inst}),{inst},I),
  inst({inst}),
