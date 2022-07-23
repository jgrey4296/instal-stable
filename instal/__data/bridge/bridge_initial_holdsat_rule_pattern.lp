%% initially %
%%
% no creation event

holdsat(live({bridge}),{bridge},I) :- start(I), bridge({bridge}).
holdsat(perm(null),{bridge},I) :- start(I), bridge({bridge}).

% initially: {x}
% condition: {x}

holdsat({inf},{bridge},I) :-
  not holdsat(live({bridge}),{bridge}),
  bridge({bridge}),
  source({source}, {bridge}),
  sink({sink}, {bridge}),
  start(I).
