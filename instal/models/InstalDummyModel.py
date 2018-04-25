import time
from typing import IO, List

from instal.clingo import Function, Symbol

from instal.instalexceptions import InstalRuntimeError
from .InstalModel import InstalModel
from .Oracle import Oracle
from instal import InstalFile
from instal.parser.InstalParserNew import InstalParserNew

class InstalDummyModel(InstalModel):
    """
        InstalMultiShotModel
        Deals with multi shot solving - instance of InstalModel.
        Used for instalquery.
    """

    def __init__(self,ial_files : List[InstalFile], bridge_files : List[InstalFile], lp_files : List[InstalFile],
        domain_files : List[InstalFile], fact_files : List[InstalFile],
        verbose : int = 0, answer_set : int = 0, length : int = 1, number : int = 1):
        super(InstalDummyModel, self).__init__(ial_files,bridge_files,lp_files,domain_files,fact_files)
        # at this point we know it compiles - do the inspection bit
        parser_wrapper = InstalParserNew()

        instal_dictionary = parser_wrapper.get_instal_dictionary(ial_files, bridge_files)
        irs_dictionary = parser_wrapper.parse(instal_dictionary)
        types = set()
        result = {
            "institutions" : {}
        }
        for i in irs_dictionary["institution_ir"]:
            for t in i["contents"]["types"]: types.add(t)
            name = i["contents"]["names"]["institution"]
            result["institutions"][name] = {
                "fluents" : i["contents"]["fluents"],
                "noninertial_fluents" : i["contents"]["noninertial_fluents"],
                "exevents" : i["contents"]["exevents"],
                "inevents" : i["contents"]["inevents"],
                "vievents" : i["contents"]["vievents"],
                "obligation_fluents" : i["contents"]["obligation_fluents"]
            }

        result["types"] = list(types)
        self.inspection = result


    def solve(self, query_events : List[Symbol]):
        raise NotImplementedError

    def get_declarations(self):
        return self.inspection