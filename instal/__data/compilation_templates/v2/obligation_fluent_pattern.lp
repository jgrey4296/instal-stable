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
inertialFluentChange(obligation(${name}, R, D, V), ${inst}, I, C) :- inertialFluentChange(${name}(R, D, V), ${inst}, I, C).
inertialFluentChange(${name}(R, D, V), ${inst}, I, C)             :- inertialFluentChange(obligation(${name}, R, D, V), ${inst}, I, C).
