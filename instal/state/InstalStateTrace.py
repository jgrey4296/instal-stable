import io
import os
from typing import List, Dict

import simplejson as json
from instal.clingo import Symbol

from instal.state.InstalState import InstalState


class InstalStateTrace(object):
    def __init__(self):
        self.trace = [] # type: List[InstalState]
        self.filename = None # type: str

    @classmethod
    def state_trace_from_json(cls, json : List[Dict],filename : str = None) -> "InstalStateTrace":
        trace = InstalStateTrace()
        trace.filename = filename
        for d in json:
            trace.append_from_json(d)
        return trace

    @classmethod
    def state_trace_from_json_file(cls, filename : str) -> "InstalStateTrace":
        with io.open(filename, "r") as jf:
            return cls.state_trace_from_json(json.load(jf),filename=filename)

    @classmethod
    def state_trace_from_list(cls, state : List[List[Symbol]], metadata : dict = None) -> "InstalStateTrace":
        # It'd be nice if this dealt with the timestep metadata
        trace = InstalStateTrace()
        for s in state:
            step_metadata = metadata.copy()
            trace.append_from_list(s, metadata=step_metadata)
        return trace

    def append_from_list(self, lst : List[Symbol], metadata : dict = None) -> None:
        self.trace.append(InstalState.state_from_list(lst, metadata=metadata))

    def append_from_json(self, json : dict) -> None:
        self.trace.append(InstalState.state_from_json(json))

    def to_json(self) -> List[Dict]:
        return [s.to_json() for s in self.trace]

    def to_json_file(self, filename):
        with io.open(filename, "w") as jf:
            print(json.dumps(self.to_json(),
                             sort_keys=True, separators=(',', ':')), file=jf)

    def get_json_filename(self, filename : str = "", base_dir : str = "") -> str:
        last = self.trace[-1]
        fn = ""
        if base_dir and not filename:
            return base_dir + "/" + "{}_{}_of_{}.json".format(last.metadata.get("pid"), last.metadata.get("answer_set_n"), last.metadata.get("answer_set_of"))
        elif last.metadata.get("answer_set_of",0) > 1:
            return ("" if not base_dir else base_dir + "/") + "{}_{}_of_{}.json".format(os.path.splitext(filename)[0], last.metadata.get("answer_set_n"), last.metadata.get("answer_set_of"))
        else:
            return ("" if not base_dir else base_dir + "/") + filename

    def to_str(self, show_perms=True, show_pows=True, show_cross=True) -> str:
        # Should string out contain some annotations? Maybe prefixed with % ?
        string_out = ""
        last = self.trace[-1]
        string_out += "% Answer Set {} of {}.\n".format(last.metadata.get("answer_set_n"),last.metadata.get("answer_set_of"))
        timestep = 1
        for s in self.trace[1:]:
            string_out += "\n% Timestep {}.\n".format(timestep)
            string_out += s.to_str(show_perms=show_perms, show_pows=show_pows, show_cross=show_cross)
            timestep += 1
        return string_out

    def check_trace_for(self, conditions) -> int:
        # Used for test cases.
        pass

    def last_state(self) -> InstalState:
        return self.trace[-1]

    def check_conditions(self, conditions: list, verbose: int=2) -> int:
        """A wrapper for check_trace_for that checks if the length of the trace and conditions are the same.
        """
        errors = 0
        if len(self.trace) == len(conditions):
            offset = 0
        elif len(self.trace) == len(conditions) + 1:
            offset = 1
        else:
            raise Exception("Trace given not long enough. (Trace: {}, conditions: {})".format(
                len(self.trace), len(conditions)))
        for i in range(0, len(conditions)):
            errors += self.trace[i + offset].check_trace_for(conditions[i], verbose)
        return errors
