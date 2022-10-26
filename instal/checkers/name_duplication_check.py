##-- imports
from collections import defaultdict
from dataclasses import InitVar, dataclass, field

import warnings

import networkx
from instal.errors import (InstalParserArgumentError, InstalParserError,
                           InstalParserNotDeclaredError, InstalParserTypeError)
from instal.interfaces.checker import InstalChecker_i

##-- end imports

@dataclass
class NameDuplicationCheck(InstalChecker_i):
    """" warn on event/fluent name duplication """

    def check(self, asts):
        for inst in asts:
            if not isinstance(inst, iAST.InstitutionDefAST):
                continue

            fluents  = []
            events   = []
            typeDecs = []
            for fluent in inst.fluents:
                if str(fluent.head) in fluents:
                    self.error(f"Duplicate Fluent Declaration", fluent)

                fluents.append(str(fluent.head))

            for event in inst.events:
                if str(event.head) in events:
                    self.error(f"Duplicate Event Declaration", event)

                if str(event.head) in fluents:
                    self.error(f"Event-Fluent Name Conflict", event)

                events.append(str(event.head))

            for typeDec in inst.types:
                if str(typeDec.head) in typeDecs:
                    self.error(f"Duplicate TypeDec Declaration", typeDec)

                if str(typeDec.head) in fluents:
                    self.error(f"TypeDec-Fluent Name Conflict", typeDec)

                if str(typeDec.head) in events:
                    self.error(f"TypeDec-Event Name Conflict", typeDec)

                typeDecs.append(str(typeDec.head))
