
##-- imports
from __future__ import annotations

from pathlib import Path
import logging as logmod
from dataclasses import InitVar, dataclass, field
from typing import NewType

from instal import defaults
##-- end imports

logging = logmod.getLogger(__name__)


@dataclass
class InstalFileGroup:
    institutions : list[Path] = field(default_factory=list)
    bridges      : list[Path] = field(default_factory=list)
    domains      : list[Path] = field(default_factory=list)
    situation    : list[Path] = field(default_factory=list)
    compiled     : list[Path] = field(default_factory=list)
    query        : None|Path  = field(default=None)

    @staticmethod
    def from_targets(*targets):
        """
        Take directories and files, and create the file group
        """
        queue = [Path(x).expanduser().resolve() for x in targets]
        found = set()
        file_group = InstalFileGroup()
        while bool(queue):
            target = queue.pop()
            if not target.exists():
                logging.warning("Specified target does not exist: %s", target)
            elif target.is_dir():
                queue += [x for x in target.iterdir()]
            elif target.is_file():
                match target.suffix:
                    case defaults.COMPILED_EXT:
                        file_group.compiled.append(target)
                    case defaults.INST_EXT:
                        file_group.institutions.append(target)
                    case defaults.BRIDGE_EXT:
                        file_group.bridges.append(target)
                    case defaults.SITUATION_EXT:
                        file_group.situation.append(target)
                    case defaults.DOMAIN_EXT:
                        file_group.domains.append(target)
                    case defaults.QUERY_EXT if file_group.query is None:
                        file_group.query = target
                    case defaults.QUERY_EXT:
                        logging.warning("Multiple Queries found, ignoring: %s", target)
                    case _:
                        logging.warning("Unrecognized file type found: %s", target)

        return file_group




    def __len__(self):
        return (len(self.institutions)
                + len(self.bridges)
                + len(self.domains)
                + len(self.situation)
                + len(self.compiled)
                + (1 if self.query is not None else 0))

    def get_sources(self):
        sources = (self.institutions
                   + self.bridges
                   + self.domains
                   + self.situation)
        if self.query is not None:
            sources.append(self.query)

        return sources


    def get_compiled(self):
        return self.compiled

