% create bridge/3 instances from inst/1, source/2, and sink/2 definitions.
bridge(BridgeInst, SourceInst, SinkInst) :- inst(BridgeInst), inst(SourceInst), inst(SinkInst), source(SourceInst, BridgeInst), sink(SinkInst, BridgeInst).
