
##-- imports
from __future__ import annotations

import logging as logmod

from instal.interfaces.parser import InstalParser
from instal.parser.institution_parser import InstitutionParser
from instal.type_checker.bridge_checker import BridgeTypeChecker
from instal.type_checker.institution_checker import InstitutionTypeChecker

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class InstalJointParser(InstitutionParser):
    """
        InstalParserNew
        Implementation of ABC InstalParserWrapper for the 2017 InstAL parser.
    """

    def __init__(self):
        super().__init__()
        self.all_lists = {}

    def parse_institution(self, ial_text):
        parser = InstitutionParser()
        parser.parse(ial_text)
        ir = parser.get_parsed_output()
        type_checker = InstitutionTypeChecker(ir)
        type_checker.check_types()
        return ir

    def parse_bridge(self, bridge_text, ial_ir):
        parser = InstitutionParser()
        parser.instal_parse(bridge_text)
        bridge_IR = parser.get_parsed_output()
        type_checker = BridgeTypeChecker(bridge_IR)
        type_checker.check_types(other_institutions=ial_ir)

        return bridge_IR
