%% Rules for Bridge {bridge}%
ifluent(live({bridge}), {bridge}).
fluent(live({bridge}), {bridge}).
bridge({bridge}).
sink({sink}, {bridge}).
source({source}, {bridge}).
:- not _preludeLoaded.
