%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Compiled Bridge
%% ${bridge}
%% From : ${source_file}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program base.

% bridge/3 (in standard prelude) is built from these:
inst(${bridge}).
source(${source}, ${bridge}).
sink(${sink}, ${bridge}).

:- not _preludeLoaded.
