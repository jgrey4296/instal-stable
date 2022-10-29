%%
%% bridge institution from p181:
%% @thesis{li14_normat_confl_detec_resol_cooper_instit_,
%%   author = {Li, TingTing},
%%   school = {University of Bath},
%%   title  = {Normative Conflict Detection and Resolution in Cooperating Institutions},
%%   year   = {2014},
%% }
%%
%
% Domain declarations for bridge %
inst(fb).
inst(us). inst(eu).
inst(bridge).
data(alice_data).
data(bob_data).
user(alice). user(bob).
party(nsa).

%
% -------------------------------PART 1-------------------------------
%
% Standard prelude for bridge
%
% fluent rules
holdsat(P,In,J) :- holdsat(P,In,I), not terminated(P,In,I), not xterminated(InS,P,In,I), next(I,J), fluent(P, In), instant(I), instant(J), inst(In;InS).
holdsat(P,In,J) :- initiated(P,In,I),next(I,J), ifluent(P, In), instant(I), instant(J), inst(In).
holdsat(P,In,J) :- initiated(P,In,I),next(I,J), oblfluent(P, In), instant(I), instant(J), inst(In).
holdsat(P,In,J) :- initiated(P,In,I),next(I,J), nifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J) :- xinitiated(InS,P,In,I), next(I,J), ifluent(P, In), instant(I), instant(J), inst(InS;In).
holdsat(P,In,J) :- xinitiated(InS,P,In,I), next(I,J), oblfluent(P, In), instant(I), instant(J), inst(InS;In).
holdsat(P,In,J) :- xinitiated(InS,P,In,I), next(I,J), nifluent(P, In), instant(I), instant(J), inst(InS;In).
true.

%
% Rules for Institution bridge
%
ifluent(live(bridge), bridge).
fluent(live(bridge), bridge).
inst(bridge).

%
% The following types were declared:
%
% Party
% Data
% User
% Inst
%
% Exogenous events
% Event: dataExportRequest (type: ex) of institution eu
event(dataExportRequest(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(dataExportRequest(User0,Data1,Party2),eu,ex)           :- user(User0),data(Data1),party(Party2).
evinst(dataExportRequest(User0,Data1,Party2),eu)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(dataExportRequest(User0,Data1,Party2)), eu)      :- user(User0),data(Data1),party(Party2).
fluent(perm(dataExportRequest(User0,Data1,Party2)), eu)       :- user(User0),data(Data1),party(Party2).
event(viol(dataExportRequest(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(dataExportRequest(User0,Data1,Party2)), eu, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(dataExportRequest(User0,Data1,Party2)),eu)        :- user(User0),data(Data1),party(Party2).

% Event: dataExport (type: ex) of institution eu
event(dataExport(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(dataExport(User0,Data1,Party2),eu,ex)           :- user(User0),data(Data1),party(Party2).
evinst(dataExport(User0,Data1,Party2),eu)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(dataExport(User0,Data1,Party2)), eu)      :- user(User0),data(Data1),party(Party2).
fluent(perm(dataExport(User0,Data1,Party2)), eu)       :- user(User0),data(Data1),party(Party2).
event(viol(dataExport(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(dataExport(User0,Data1,Party2)), eu, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(dataExport(User0,Data1,Party2)),eu)        :- user(User0),data(Data1),party(Party2).

% Event: dataCollect (type: ex) of institution us
event(dataCollect(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(dataCollect(User0,Data1,Party2),us,ex)           :- user(User0),data(Data1),party(Party2).
evinst(dataCollect(User0,Data1,Party2),us)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(dataCollect(User0,Data1,Party2)), us)      :- user(User0),data(Data1),party(Party2).
fluent(perm(dataCollect(User0,Data1,Party2)), us)       :- user(User0),data(Data1),party(Party2).
event(viol(dataCollect(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(dataCollect(User0,Data1,Party2)), us, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(dataCollect(User0,Data1,Party2)),us)        :- user(User0),data(Data1),party(Party2).

% Event: share (type: ex) of institution eu
event(share(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(share(User0,Data1,Party2),eu,ex)           :- user(User0),data(Data1),party(Party2).
evinst(share(User0,Data1,Party2),eu)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(share(User0,Data1,Party2)), eu)      :- user(User0),data(Data1),party(Party2).
fluent(perm(share(User0,Data1,Party2)), eu)       :- user(User0),data(Data1),party(Party2).
event(viol(share(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(share(User0,Data1,Party2)), eu, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(share(User0,Data1,Party2)),eu)        :- user(User0),data(Data1),party(Party2).

% Event: share (type: ex) of institution fb
event(share(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(share(User0,Data1,Party2),fb,ex)           :- user(User0),data(Data1),party(Party2).
evinst(share(User0,Data1,Party2),fb)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(share(User0,Data1,Party2)), fb)      :- user(User0),data(Data1),party(Party2).
fluent(perm(share(User0,Data1,Party2)), fb)       :- user(User0),data(Data1),party(Party2).
event(viol(share(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(share(User0,Data1,Party2)), fb, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(share(User0,Data1,Party2)),fb)        :- user(User0),data(Data1),party(Party2).

% Event: share (type: ex) of institution us
event(share(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(share(User0,Data1,Party2),us,ex)           :- user(User0),data(Data1),party(Party2).
evinst(share(User0,Data1,Party2),us)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(share(User0,Data1,Party2)), us)      :- user(User0),data(Data1),party(Party2).
fluent(perm(share(User0,Data1,Party2)), us)       :- user(User0),data(Data1),party(Party2).
event(viol(share(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(share(User0,Data1,Party2)), us, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(share(User0,Data1,Party2)),us)        :- user(User0),data(Data1),party(Party2).

% Event: shareRequest (type: ex) of institution fb
event(shareRequest(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(shareRequest(User0,Data1,Party2),fb,ex)           :- user(User0),data(Data1),party(Party2).
evinst(shareRequest(User0,Data1,Party2),fb)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(shareRequest(User0,Data1,Party2)), fb)      :- user(User0),data(Data1),party(Party2).
fluent(perm(shareRequest(User0,Data1,Party2)), fb)       :- user(User0),data(Data1),party(Party2).
event(viol(shareRequest(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(shareRequest(User0,Data1,Party2)), fb, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(shareRequest(User0,Data1,Party2)),fb)        :- user(User0),data(Data1),party(Party2).

% Event: deadline (type: ex) of institution fb
event(deadline)                  :- true.
evtype(deadline,fb,ex)           :- true.
evinst(deadline,fb)              :- true.
ifluent(perm(deadline), fb)      :- true.
fluent(perm(deadline), fb)       :- true.
event(viol(deadline))            :- true.
evtype(viol(deadline), fb, viol) :- true.
evinst(viol(deadline),fb)        :- true.

% Event: deadline (type: ex) of institution us
event(deadline)                  :- true.
evtype(deadline,us,ex)           :- true.
evinst(deadline,us)              :- true.
ifluent(perm(deadline), us)      :- true.
fluent(perm(deadline), us)       :- true.
event(viol(deadline))            :- true.
evtype(viol(deadline), us, viol) :- true.
evinst(viol(deadline),us)        :- true.

% Event: dataCollectRequest (type: ex) of institution us
event(dataCollectRequest(User0,Data1,Party2))                  :- user(User0),data(Data1),party(Party2).
evtype(dataCollectRequest(User0,Data1,Party2),us,ex)           :- user(User0),data(Data1),party(Party2).
evinst(dataCollectRequest(User0,Data1,Party2),us)              :- user(User0),data(Data1),party(Party2).
ifluent(perm(dataCollectRequest(User0,Data1,Party2)), us)      :- user(User0),data(Data1),party(Party2).
fluent(perm(dataCollectRequest(User0,Data1,Party2)), us)       :- user(User0),data(Data1),party(Party2).
event(viol(dataCollectRequest(User0,Data1,Party2)))            :- user(User0),data(Data1),party(Party2).
evtype(viol(dataCollectRequest(User0,Data1,Party2)), us, viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(dataCollectRequest(User0,Data1,Party2)),us)        :- user(User0),data(Data1),party(Party2).

%
% null event for unknown events
% Event: null (type: ex)
event(null).
evtype(null,bridge,ex).
evinst(null,bridge).
ifluent(perm(null), bridge).
fluent(perm(null), bridge).
event(viol(null)).
evtype(viol(null),bridge,viol).
evinst(viol(null),bridge).

% Institutional events
% Event: intShareRequest (type: in) of institution fb
event(intShareRequest(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intShareRequest(User0,Data1,Party2),fb,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intShareRequest(User0,Data1,Party2),fb)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(fb,intShareRequest(User0,Data1,Party2)),fb)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intShareRequest(User0,Data1,Party2)),fb)     :- user(User0),data(Data1),party(Party2).
fluent(pow(fb,intShareRequest(User0,Data1,Party2)),fb)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intShareRequest(User0,Data1,Party2)),fb)      :- user(User0),data(Data1),party(Party2).
event(viol(intShareRequest(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intShareRequest(User0,Data1,Party2)),fb,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intShareRequest(User0,Data1,Party2)),fb)      :- user(User0),data(Data1),party(Party2).

% Event: intDataExportRequest (type: in) of institution eu
event(intDataExportRequest(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intDataExportRequest(User0,Data1,Party2),eu,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intDataExportRequest(User0,Data1,Party2),eu)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(eu,intDataExportRequest(User0,Data1,Party2)),eu)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intDataExportRequest(User0,Data1,Party2)),eu)     :- user(User0),data(Data1),party(Party2).
fluent(pow(eu,intDataExportRequest(User0,Data1,Party2)),eu)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intDataExportRequest(User0,Data1,Party2)),eu)      :- user(User0),data(Data1),party(Party2).
event(viol(intDataExportRequest(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intDataExportRequest(User0,Data1,Party2)),eu,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intDataExportRequest(User0,Data1,Party2)),eu)      :- user(User0),data(Data1),party(Party2).

% Event: intDataCollectRequest (type: in) of institution us
event(intDataCollectRequest(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intDataCollectRequest(User0,Data1,Party2),us,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intDataCollectRequest(User0,Data1,Party2),us)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(us,intDataCollectRequest(User0,Data1,Party2)),us)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intDataCollectRequest(User0,Data1,Party2)),us)     :- user(User0),data(Data1),party(Party2).
fluent(pow(us,intDataCollectRequest(User0,Data1,Party2)),us)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intDataCollectRequest(User0,Data1,Party2)),us)      :- user(User0),data(Data1),party(Party2).
event(viol(intDataCollectRequest(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intDataCollectRequest(User0,Data1,Party2)),us,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intDataCollectRequest(User0,Data1,Party2)),us)      :- user(User0),data(Data1),party(Party2).

% Event: intShare (type: in) of institution eu
event(intShare(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intShare(User0,Data1,Party2),eu,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intShare(User0,Data1,Party2),eu)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(eu,intShare(User0,Data1,Party2)),eu)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intShare(User0,Data1,Party2)),eu)     :- user(User0),data(Data1),party(Party2).
fluent(pow(eu,intShare(User0,Data1,Party2)),eu)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intShare(User0,Data1,Party2)),eu)      :- user(User0),data(Data1),party(Party2).
event(viol(intShare(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intShare(User0,Data1,Party2)),eu,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intShare(User0,Data1,Party2)),eu)      :- user(User0),data(Data1),party(Party2).

% Event: intShare (type: in) of institution fb
event(intShare(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intShare(User0,Data1,Party2),fb,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intShare(User0,Data1,Party2),fb)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(fb,intShare(User0,Data1,Party2)),fb)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intShare(User0,Data1,Party2)),fb)     :- user(User0),data(Data1),party(Party2).
fluent(pow(fb,intShare(User0,Data1,Party2)),fb)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intShare(User0,Data1,Party2)),fb)      :- user(User0),data(Data1),party(Party2).
event(viol(intShare(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intShare(User0,Data1,Party2)),fb,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intShare(User0,Data1,Party2)),fb)      :- user(User0),data(Data1),party(Party2).

% Event: intShare (type: in) of institution us
event(intShare(User0,Data1,Party2))                :- user(User0),data(Data1),party(Party2).
evtype(intShare(User0,Data1,Party2),us,inst)       :- user(User0),data(Data1),party(Party2).
evinst(intShare(User0,Data1,Party2),us)            :- user(User0),data(Data1),party(Party2).
ifluent(pow(us,intShare(User0,Data1,Party2)),us)   :- user(User0),data(Data1),party(Party2).
ifluent(perm(intShare(User0,Data1,Party2)),us)     :- user(User0),data(Data1),party(Party2).
fluent(pow(us,intShare(User0,Data1,Party2)),us)    :- user(User0),data(Data1),party(Party2).
fluent(perm(intShare(User0,Data1,Party2)),us)      :- user(User0),data(Data1),party(Party2).
event(viol(intShare(User0,Data1,Party2)))          :- user(User0),data(Data1),party(Party2).
evtype(viol(intShare(User0,Data1,Party2)),us,viol) :- user(User0),data(Data1),party(Party2).
evinst(viol(intShare(User0,Data1,Party2)),us)      :- user(User0),data(Data1),party(Party2).

%
% Violation events of institution {inst}
%
% Event: noncompliance (type: in)
event(noncompliance(User0))          :- user(User0).
evtype(noncompliance(User0),fb,viol) :- user(User0).
evinst(noncompliance(User0),fb)      :- user(User0).

% Event: noncompliance (type: in)
event(noncompliance(User0))          :- user(User0).
evtype(noncompliance(User0),us,viol) :- user(User0).
evinst(noncompliance(User0),us)      :- user(User0).

%
% inertial fluents
%
ifluent(securityDep(Party0),us)     :- party(Party0).
fluent(securityDep(Party0),us)      :- party(Party0).
ifluent(protected(Data0,Party1),eu) :- data(Data0),party(Party1).
fluent(protected(Data0,Party1),eu)  :- data(Data0),party(Party1).
ifluent(protected(Data0,Party1),fb) :- data(Data0),party(Party1).
fluent(protected(Data0,Party1),fb)  :-data(Data0),party(Party1).
ifluent(protected(Data0,Party1),us) :-data(Data0),party(Party1).
fluent(protected(Data0,Party1),us)  :-data(Data0),party(Party1).
ifluent(interested(User0,Data1),eu) :-user(User0),data(Data1).
fluent(interested(User0,Data1),eu)  :-user(User0),data(Data1).
ifluent(interested(User0,Data1),us) :-user(User0),data(Data1).
fluent(interested(User0,Data1),us)  :-user(User0),data(Data1).
ifluent(trusted(Party0),fb)         :-party(Party0).
fluent(trusted(Party0),fb)          :-party(Party0).

%
% Translation of the obligation fluent obl(share(User0,Data1,Party2),
% deadline,noncompliance(User3)) of us:
%
oblfluent(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)), us)   :- event(share(User0,Data1,Party2)), event(deadline), event(noncompliance(User3)), user(User0),data(Data1),party(Party2), true,user(User3),inst(us).
fluent(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)), us)      :- event(share(User0,Data1,Party2)), event(deadline), event(noncompliance(User3)), user(User0),data(Data1),party(Party2), true,user(User3),inst(us).
terminated(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)),us,I) :- event(share(User0,Data1,Party2)), occurred(share(User0,Data1,Party2),us,I), event(deadline), holdsat(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)),us,I), event(noncompliance(User3)), user(User0),data(Data1),party(Party2), true,user(User3),inst(us).
terminated(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)),us,I) :- event(share(User0,Data1,Party2)), event(deadline), occurred(deadline,us,I), holdsat(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)),us,I), event(noncompliance(User3)), user(User0),data(Data1),party(Party2), true,user(User3),inst(us).
occurred(noncompliance(User3),us,I)                                           :- event(share(User0,Data1,Party2)), event(deadline), occurred(deadline,us,I), holdsat(obl(share(User0,Data1,Party2),deadline,noncompliance(User3)),us,I), event(noncompliance(User3)), user(User0),data(Data1),party(Party2), true,user(User3),inst(us).

%
% cross fluents
%
fluent(gpow(I0,dataCollect(User0,Data1,Party2),I1), bridge)                           :- inst(I0; I1; bridge), event(dataCollect(User0,Data1,Party2)), evinst(dataCollect(User0,Data1,Party2), I1), evtype(dataCollect(User0,Data1,Party2), I1, ex), user(User0),data(Data1) party(Party2).
ifluent(gpow(I0,dataCollect(User0,Data1,Party2),I1), bridge)                          :- inst(I0; I1; bridge), event(dataCollect(User0,Data1,Party2)), evinst(dataCollect(User0,Data1,Party2), I1), evtype(dataCollect(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
fluent(gpow(I0,dataExport(User0,Data1,Party2),I1), bridge)                            :- inst(I0; I1; bridge), event(dataExport(User0,Data1,Party2)), evinst(dataExport(User0,Data1,Party2), I1), evtype(dataExport(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
ifluent(gpow(I0,dataExport(User0,Data1,Party2),I1), bridge)                           :- inst(I0; I1; bridge), event(dataExport(User0,Data1,Party2)), evinst(dataExport(User0,Data1,Party2), I1), evtype(dataExport(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
fluent(gpow(I0,dataCollectRequest(User0,Data1,Party2),I1), bridge)                    :- inst(I0; I1; bridge), event(dataCollectRequest(User0,Data1,Party2)), evinst(dataCollectRequest(User0,Data1,Party2), I1), evtype(dataCollectRequest(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
ifluent(gpow(I0,dataCollectRequest(User0,Data1,Party2),I1), bridge)                   :- inst(I0; I1; bridge), event(dataCollectRequest(User0,Data1,Party2)), evinst(dataCollectRequest(User0,Data1,Party2), I1), evtype(dataCollectRequest(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
fluent(gpow(I0,dataExportRequest(User0,Data1,Party2),I1), bridge)                     :- inst(I0; I1; bridge), event(dataExportRequest(User0,Data1,Party2)), evinst(dataExportRequest(User0,Data1,Party2), I1), evtype(dataExportRequest(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
ifluent(gpow(I0,dataExportRequest(User0,Data1,Party2),I1), bridge)                    :- inst(I0; I1; bridge), event(dataExportRequest(User0,Data1,Party2)), evinst(dataExportRequest(User0,Data1,Party2), I1), evtype(dataExportRequest(User0,Data1,Party2), I1, ex), user(User0),data(Data1), party(Party2).
fluent(ipow(I0,obl(share(User,Data,Party),deadline,noncompliance(User)),I1), bridge)  :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(obl(share(User,Data,Party),deadline,noncompliance(User)), I1).
ifluent(ipow(I0,obl(share(User,Data,Party),deadline,noncompliance(User)),I1), bridge) :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(obl(share(User,Data,Party),deadline,noncompliance(User)), I1).
ifluent(ipow(I0,obl(share(User,Data,Party),deadline,noncompliance(User)),I1), bridge) :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(obl(share(User,Data,Party),deadline,noncompliance(User)), I1).
fluent(ipow(I0,perm(share(User,Data,Party)),I1), bridge)                              :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(perm(share(User,Data,Party)), I1).
ifluent(ipow(I0,perm(share(User,Data,Party)),I1), bridge)                             :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(perm(share(User,Data,Party)), I1).
fluent(tpow(I0,perm(share(User,Data,Party)),I1), bridge)                              :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(perm(share(User,Data,Party)), I1).
ifluent(tpow(I0,perm(share(User,Data,Party)),I1), bridge)                             :- inst(I0; I1; bridge), party(Party), data(Data), user(User), fluent(perm(share(User,Data,Party)), I1).

%
% -------------------------------PART 2------------------------------- %
%
% cross generate rules
%
%
%
% Translation of intShare(User,Data,Party) of eu
%   xgenerates dataCollect(User,Data,Party) of us if [] in
occurred(dataCollect(User,Data,Party),us,I) :- occurred(intShare(User,Data,Party),eu,I), holdsat(gpow(eu,dataCollect(User,Data,Party),us),bridge,I), inst(us;eu), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intShare(User,Data,Party) of fb
%   xgenerates dataCollect(User,Data,Party) of us if [] in
occurred(dataCollect(User,Data,Party),us,I) :- occurred(intShare(User,Data,Party),fb,I), holdsat(gpow(fb,dataCollect(User,Data,Party),us),bridge,I), inst(us;fb), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intShare(User,Data,Party) of fb
%   xgenerates dataExport(User,Data,Party) of eu if [] in
occurred(dataExport(User,Data,Party),eu,I) :- occurred(intShare(User,Data,Party),fb,I), holdsat(gpow(fb,dataExport(User,Data,Party),eu),bridge,I), inst(eu;fb), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intShare(User,Data,Party) of us
%   xgenerates dataExport(User,Data,Party) of eu if [] in
occurred(dataExport(User,Data,Party),eu,I) :- occurred(intShare(User,Data,Party),us,I), holdsat(gpow(us,dataExport(User,Data,Party),eu),bridge,I), inst(eu;us), party(Party), data(Data), user(User), inst(bridge), instant(I).
%
% Translation of intShareRequest(User,Data,Party) of fb
% xgenerates dataCollectRequest(User,Data,Party) of us if [] in occurred(dataCollectRequest(User,Data,Party),us,I) :-
occurred(intShareRequest(User,Data,Party),fb,I), holdsat(gpow(fb,dataCollectRequest(User,Data,Party),us),bridge,I), inst(us;fb), party(Party), data(Data), user(User), inst(bridge), instant(I).
%
% Translation of intShareRequest(User,Data,Party) of fb
%    xgenerates dataExportRequest(User,Data,Party) of eu if [] in
occurred(dataExportRequest(User,Data,Party),eu,I) :- occurred(intShareRequest(User,Data,Party),fb,I), holdsat(gpow(fb,dataExportRequest(User,Data,Party),eu),bridge,I), inst(eu;fb), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% cross initiation rules
% %
% Translation of intDataCollectRequest(User,Data,Party) of us xinitiates
% [’perm’, [’share’, [’User’, ’Data’, ’Party’]]]
% of eu if [’and’, [’interested’, [’User’, ’Data’]], [’securityDep’, [’Party’]]]
%
xinitiated(us, perm(share(User,Data,Party)),eu,I) :- occurred(intDataCollectRequest(User,Data,Party),us,I), holdsat(ipow(us, perm(share(User,Data,Party)), eu), bridge, I), holdsat(live(bridge),bridge,I), inst(bridge), inst(eu;us), holdsat(interested(User,Data),us,I), holdsat(securityDep(Party),us,I), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intDataCollectRequest(User,Data,Party) of us xinitiates
% [’perm’, [’share’, [’User’, ’Data’, ’Party’]]]
% of fb if [’and’, [’interested’, [’User’, ’Data’]], [’securityDep’, [’Party’]]]
%
xinitiated(us, perm(share(User,Data,Party)),fb,I) :- occurred(intDataCollectRequest(User,Data,Party),us,I), holdsat(ipow(us, perm(share(User,Data,Party)), fb), bridge, I), holdsat(live(bridge),bridge,I), inst(bridge), inst(fb;us), holdsat(interested(User,Data),us,I), holdsat(securityDep(Party),us,I), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intDataCollectRequest(User,Data,Party) of us xinitiates
% [’obl’, [[’share’, [’User’, ’Data’, ’Party’]], [’deadline’, []], [’noncompliance’,
% [’User’]]]] of fb if [’and’, [’interested’, [’User’, ’Data’]], [’securityDep’,
%[’Party’]]]
%
xinitiated(us, obl(share(User,Data,Party),deadline,noncompliance(User)),fb,I) :- occurred(intDataCollectRequest(User,Data,Party),us,I), holdsat(ipow(us, obl(share(User,Data,Party),deadline,noncompliance(User)), fb), bridge, I), holdsat(live(bridge),bridge,I), inst(bridge), inst(fb;us), holdsat(interested(User,Data),us,I), holdsat(securityDep(Party),us,I), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% cross termination rules
%
%
% Translation of intDataExportRequest(User,Data,Party) of eu xterminates
% [’perm’, [’share’, [’User’, ’Data’, ’Party’]]]
% of fb if [’not’, [’protected’, [’Data’, ’Party’]]]
%
xterminated(eu, perm(share(User,Data,Party)), fb, I) :- occurred(intDataExportRequest(User,Data,Party),eu,I), holdsat(tpow(eu, perm(share(User,Data,Party)), fb), bridge, I), holdsat(live(bridge),bridge,I), inst(bridge), inst(fb;eu), not holdsat(protected(Data,Party),eu,I), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% Translation of intDataExportRequest(User,Data,Party) of eu xterminates
% [’perm’, [’share’, [’User’, ’Data’, ’Party’]]]
% of us if [’not’, [’protected’, [’Data’, ’Party’]]]
%
xterminated(eu, perm(share(User,Data,Party)), us, I) :- occurred(intDataExportRequest(User,Data,Party),eu,I), holdsat(tpow(eu, perm(share(User,Data,Party)), us), bridge, I), holdsat(live(bridge),bridge,I), inst(bridge), inst(us;eu), not holdsat(protected(Data,Party),eu,I), party(Party), data(Data), user(User), inst(bridge), instant(I).

%
% -------------------------------PART 3-------------------------------
%
% initially
%
% no creation event
holdsat(live(bridge),bridge,I) :- start(I), inst(bridge).
holdsat(perm(null),bridge,I) :- start(I), inst(bridge).

% initially: gpow(fb,dataExportRequest(User,Data,Party),eu)
holdsat(gpow(fb,dataExportRequest(User,Data,Party),eu),bridge,I) :- party(Party), data(Data), user(User), inst(eu; fb), inst(bridge), start(I).

% initially: gpow(fb,dataCollectRequest(User,Data,Party),us)
holdsat(gpow(fb,dataCollectRequest(User,Data,Party),us),bridge,I) :- party(Party), data(Data), user(User), inst(us; fb), inst(bridge), start(I).

% initially: gpow(fb,dataExport(User,Data,Party),eu)
holdsat(gpow(fb,dataExport(User,Data,Party),eu),bridge,I) :- party(Party), data(Data), user(User), inst(eu; fb), inst(bridge), start(I).

% initially: gpow(fb,dataCollect(User,Data,Party),us)
holdsat(gpow(fb,dataCollect(User,Data,Party),us),bridge,I) :- party(Party), data(Data), user(User), inst(us; fb), inst(bridge), start(I).

% initially: tpow(eu,perm(share(User,Data,Party)),fb)
holdsat(tpow(eu,perm(share(User,Data,Party)),fb),bridge,I) :- party(Party), data(Data), user(User), inst(fb; eu), inst(bridge), start(I).

% initially: ipow(us,perm(share(User,Data,Party)),fb)
holdsat(ipow(us,perm(share(User,Data,Party)),fb),bridge,I) :- party(Party), data(Data), user(User), inst(fb; us), inst(bridge), start(I).

% initially: ipow(us,obl(share(User,Data,Party),deadline,noncompliance(User)),fb)
holdsat(ipow(us,obl(share(User,Data,Party),deadline,noncompliance(User)),fb), bridge,I) :- party(Party), data(Data), user(User), inst(fb; us), inst(bridge), start(I).

% initially: securityDep(nsa)
holdsat(securityDep(nsa),bridge,I) :- inst(bridge), start(I).

% initially: trusted(nsa)
holdsat(trusted(nsa),bridge,I) :- inst(bridge), start(I).

% initially: interested(bob,bob_data)
holdsat(interested(bob,bob_data),bridge,I) :- inst(bridge), start(I).

%
% End of file
