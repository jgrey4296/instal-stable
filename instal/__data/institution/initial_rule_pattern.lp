% no creation event
holdsat(live({inst}),{inst},I) :- start(I), inst({inst}).
holdsat(perm(null),{inst},I) :- start(I), inst({inst}).
holdsat(pow(null),{inst},I) :- start(I), inst({inst}).
