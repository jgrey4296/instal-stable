% initially: {x}
holdsat({inf},{inst},I) :-
  not holdsat(live({inst}),{inst}),
