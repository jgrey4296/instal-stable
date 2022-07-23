"""
instal.factparser

Use the following method to parse .iaf and .json files:
    def get_facts(self,fact_filenames):
        input: a list of file names to .iaf and .json (standard InstAL json as defined in tk) fact files.
            Note: The state of the LAST state in the JSON is used.
        output: a list of Fun objects of things that hold the initial state of the system.

Use the fact parser in the following way:
    fact_parser = FactParser()
    facts = fact_parser.get_facts(FACT_FILENAMES)
"""
##-- imports
from __future__ import annotations

import logging as logmod
import os
from io import StringIO
from typing import IO, List

from clingo import Symbol, parse_term
from instal import InstalFile
from instal.instalexceptions import InstalCompileError
from instal.instaljsonhelpers import dict_funs_to_list, trace_dicts_from_file
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

class FactParser(object):
    """
        FactParser
        See __init__.py for more details.
    """

    def __init__(self):
        pass

    def get_facts(self, fact_files: List[InstalFile]) -> List[Symbol]:
        """
        input: a set of fact filenames
        output: a list of Function objects that are true at the first timestep
        """
        initlist = []
        for factfile in fact_files:
            # name, ext = os.path.splitext(factfile.name)
            # if ext == ".iaf":
            #     initlist += self.parse_iaf_factfile(factfile.read())
            #     if ext == ".json":
            #         initlist += self.parse_json_factfile(factfile.read())
            # TODO: Something about this.
            if factfile.read()[0] == "{":
                factfile.seek(0)
                initlist += self.parse_json_factfile(factfile.read())
            else:
                factfile.seek(0)
                initlist += self.parse_iaf_factfile(factfile.read())


        return initlist

    def parse_json_factfile(self, json_file: str) -> List[Symbol]:
        """
        input: a json file
        output: a list of the facts true in the *last* step in that json file.
        (This allows restarting from an old trace.)
        """
        jsons = trace_dicts_from_file(json_file)
        if len(jsons) == 0:
            return []
        return dict_funs_to_list(jsons[-1], keys=["holdsat"])

    def parse_iaf_factfile(self, iaf_text: str) -> List[Symbol]:
        """
        input: an iaf text (as a string)
        output: a list of the facts
        """
        initlist = []
        iafIO = StringIO(iaf_text)
        for init in iafIO.readlines():
            init = init.rstrip()
            if init == '':
                continue
            term = parse_term(init)
            if term.name in ["initially"]:
                where = term.arguments[1]
                what = term.arguments[0]
                initlist = [
                    "holdsat(" + str(what) + "," + str(where) + ")"] + initlist
            else:
                raise InstalCompileError(
                    ".iaf file should be in the format initially({holdsat}, {institution})")
        return list(map(parse_term, initlist))
