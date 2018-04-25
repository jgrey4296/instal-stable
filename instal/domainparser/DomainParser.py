import re
from collections import defaultdict
from io import StringIO
from typing import List, IO

from instal.instalexceptions import InstalCompileError
from instal.instalutility import InstalFile, instal_file_name


class DomainParser(object):
    """
        DomainParser
        See __init__.py for more details.
    """

    def __init__(self):
        pass

    def get_groundings(self, domain_files: List[InstalFile]) -> defaultdict(set):
        """
        input: a list of domain filenames
        output: a defaultdict(set) of the domains from those files.
        """
        domain_texts = []
        for d in domain_files:
                domain_texts.append(
                    {"filename": instal_file_name(d), "contents": d.read()})

        domain_facts = defaultdict(set)

        for d in domain_texts:
            grounds = self.get_grounding(d["contents"])
            for t, v in grounds.items():
                domain_facts[t].update(v)

        return domain_facts

    def get_grounding(self, domain_text: str) -> defaultdict(set):
        """

        input: The domain file (as a string)
        output: that domain file's groundings as defaultdict(set)
        """
        domain_facts = defaultdict(set)
        fileIO = StringIO(domain_text)
        literal = r"([a-z|\d][a-zA-Z0-9_]*)"
        for l in fileIO.readlines():
            l = l.rstrip()
            if l == '':
                continue
            [t, r] = re.split(": ", l)
            t = t.lower()
            r = re.split(" ", r)
            for s in r:
                if not (re.search(literal, s)):
                    raise InstalCompileError(
                        "ERROR: Unrecognized literal in {x}".format(x=l))
                domain_facts[t].update([s])
        return domain_facts
