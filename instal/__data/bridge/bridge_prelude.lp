%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Compiled Bridge
%% ${bridge}
%% From : ${source_file}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% bridge/3 (in standard prelude) is built from these:
inst(${bridge}).
source(${source}, ${bridge}).
sink(${sink}, ${bridge}).

%% Rules for Bridge ${bridge} %
ifluent(live(${bridge}), ${bridge}).
fluent(live(${bridge}), ${bridge}).
sink(${sink}, ${bridge}).
source(${source}, ${bridge}).
:- not _preludeLoaded.

% no creation event
holdsat(live(${bridge}), ${bridge}, I) :- start(I), bridge(${bridge}).
holdsat(perm(null), ${bridge}, I)      :- start(I), bridge(${bridge}).
