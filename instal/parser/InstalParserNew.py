from instal.parser.instaltypechecker import InstalTypeChecker
from .InstalParserWrapper import InstalParserWrapper
from .bridgetypechecker import BridgeTypeChecker
from .instalparser import InstalParser


class InstalParserNew(InstalParserWrapper):
    """
        InstalParserNew
        Implementation of ABC InstalParserWrapper for the 2017 InstAL parser.
    """

    def __init__(self):
        super().__init__()
        self.all_lists = {}

    def parse_ial(self, ial_text):
        parser = InstalParser()
        parser.instal_parse(ial_text)
        ir_dict = parser.get_parsed_output()
        type_checker = InstalTypeChecker(ir_dict)
        type_checker.check_types()
        return ir_dict

    def parse_bridge(self, bridge_text, ial_ir):
        parser = InstalParser()
        parser.instal_parse(bridge_text)
        bridge_IR_dict = parser.get_parsed_output()
        type_checker = BridgeTypeChecker(bridge_IR_dict)
        type_checker.check_types(other_institutions=ial_ir)

        return bridge_IR_dict
