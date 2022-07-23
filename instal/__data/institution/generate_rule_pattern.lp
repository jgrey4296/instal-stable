% Translation of {exev} generates {inev} if {condition} in {time}
occurred({inev},{inst},I{time}) :-
  occurred({exev},{inst},I),
  not occurred(viol({exev}),{inst},I),
