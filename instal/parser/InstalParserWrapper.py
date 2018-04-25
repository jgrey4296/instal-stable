from abc import ABCMeta
from typing import IO, List
from instal import InstalFile, instal_file_name
class InstalParserWrapper(metaclass=ABCMeta):
    """
        InstalParserWrapper
        See __init__.py for more details.
    """

    def __init__(self):
        pass

    def parse(self, instal_dictionary, save_output_files=None):
        instal_dictionary_ir = {"institution_ir": [], "bridge_ir": []}
        for i in instal_dictionary["institutions"]:
            ir = self.parse_ial(i["contents"])
            instal_dictionary_ir["institution_ir"].append(
                {"filename": i["filename"], "contents": ir})
            if save_output_files:
                raise NotImplementedError(
                    "Saving InstAL IR is not available at this time.")

        for b in instal_dictionary["bridge"]:
            ir = self.parse_bridge(
                b["contents"], instal_dictionary_ir["institution_ir"])
            instal_dictionary_ir["bridge_ir"].append(
                {"filename": b["filename"], "contents": ir})

            if save_output_files:
                raise NotImplementedError(
                    "Saving InstAL IR is not available at this time.")

        return instal_dictionary_ir

    def parse_ial(self, ial_text):
        raise NotImplementedError

    def parse_bridge(self, bridge_text, ial_ir):
        raise NotImplementedError

    def get_instal_dictionary(self, input_files : List[InstalFile], bridge_files : List[InstalFile]):
        instal_dict = {"institutions": [], "bridge": []}
        for i in input_files:
            i.seek(0)
            instal_dict["institutions"].append(self.get_model_text(i))

        for b in bridge_files:
            b.seek(0)
            instal_dict["bridge"].append(self.get_model_text(b))

        return instal_dict

    def get_model_text(self, model_file : InstalFile) -> dict:
        return {"filename": instal_file_name(model_file), "contents": model_file.read()}
