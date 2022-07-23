%% cross generate rules %
%%
% Translation of {inev} of {sinst} xgenerates {x} of {dinst} if {condition} in {time}\n
occurred({x},{dinst},I{time}) :-
  occurred({inev},{sinst},I),
  holdsat(gpow({sinst},{x},{dinst}),{inst},I{time}),
  inst({sinst}),
  source({sinst}, {inst}),
  inst({dinst}),
  sink({dinst}, {inst}),
  bridge({inst}),
