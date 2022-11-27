% Translation of ${source_event} generates ${result_event} if [condition] (in ${delay})
%% Ex Event generates Inst Event:
occurred(${result_event}, ${inst}, I${delay})            :- instant(I),
                                                            institution(${inst}),
                                                            eventType(${source_event}, ${inst}, ex),
                                                            eventType(${result_event}, ${inst}, inst),
                                                            holdsat(deontic(power, ${result_event}), ${inst}, I),
                                                            observed(${source_event}, I),
                                                            ${rhs}.

%% Inst Event Generates Inst Event
occurred(${result_event}, ${inst}, I${delay})            :- instant(I),
                                                            institution(${inst}),
                                                            eventType(${source_event}, ${inst}, inst),
                                                            eventType(${result_event}, ${inst}, inst),
                                                            holdsat(deontic(power, ${result_event}), ${inst}, I),
                                                            occurred(${source_event}, ${inst}, I),
                                                            ${rhs}.

%% Unempowered event generation
occurred(_unempoweredEvent(${result_event}), ${inst}, I) :- instant(I),
                                                            institution(${inst}),
                                                            eventType(${source_event}, ${inst}, ex),
                                                            eventType(${result_event}, ${inst}, inst),
                                                            not holdsat(deontic(power, ${result_event}), ${inst}, I),
                                                            observed(${source_event}, I),
                                                            ${rhs}.

occurred(_unempoweredEvent(${result_event}), ${inst}, I) :- instant(I),
                                                            institution(${inst}),
                                                            eventType(${source_event}, ${inst}, inst),
                                                            eventType(${result_event}, ${inst}, inst),
                                                            not holdsat(deontic(power, ${result_event}), ${inst}, I),
                                                            occurred(${source_event}, ${inst}, I),
                                                            ${rhs}.

%% Unpermitted event generation
occurred(_unpermittedEvent(${result_event}), ${inst}, I) :- instant(I),
                                                            institution(${inst}),
                                                            eventType(${result_event}, ${inst}, inst),
                                                            holdsat(deontic(power, ${result_event}), ${inst}, I),
                                                            not holdsat(deontic(permitted, ${result_event}), ${inst}, I),
                                                            occurred(${result_event}, ${inst}, I),
                                                            ${rhs}.
