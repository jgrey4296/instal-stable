%% obligation fluent: ${fluent} %
obligationFluent(obligation(${name}, ${requirement}, ${deadline}, ${violation}), ${inst}) :- institution(${inst}),
                                                                                             eventType(${requirement}, ${inst}, inst),
                                                                                             eventType(${deadline}, ${inst}, inst),
                                                                                             eventType(${violation}, ${inst}, inst),
                                                                                             ${rhs}.

obligationType(${name}, ${obType}, ${inst}).

% as function heads can't be variables,
% convert name(...) to obligation(name ...) for internal use
inertialFluent(${name}(${requirement}, ${deadline}, ${violation}), ${inst}) :- institution(${inst}).

% but make sure they sync:
initiated(obligation(${name}, R, D, V), Ins, I) :- instant(I),
                                                   institution(${inst}),
                                                   initiated(${name}(R, D, V), Ins, I).

terminated(obligation(${name}, R, D, V), Ins, I) :- instant(I),
                                                    institution(${inst}),
                                                    terminated(${name}(R, D, V), Ins, I).

initiated(${name}(R, D, V), Ins, I) :- instant(I),
                                       institution(${inst}),
                                       initiated(obligation(${name}, R, D, V), Ins, I).

terminated(${name}(R, D, V), Ins, I) :- instant(I),
                                        institution(${inst}),
                                        terminated(obligation(${name}, R, D, V), Ins, I).
