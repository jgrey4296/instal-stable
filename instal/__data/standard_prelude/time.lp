%%-- time
#const horizon = 5.
start(0).
instant(0..T) :- final(T).
next(T, T+1) :- instant(T).
final(horizon).
%%-- end time
