%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Compiled Institution
%% ${institution}
%% From    : ${source_file}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program base.

% Rules for Institution ${institution} %
inst(${institution}).
ifluent(live(${institution}), ${institution}).
fluent(live(${institution}), ${institution}).

:- not _preludeLoaded.
