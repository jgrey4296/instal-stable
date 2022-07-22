#! /usr/bin/env python

from .instalargparse import getqueryargs, check_args, buildqueryargparser
from .instalquery import instal_query_with_args


def instal_solve():
    args, unk = getqueryargs()
    instal_solve_with_args(args, unk)


def instal_solve_keyword(bridge_files=None, domain_files=None, fact_files=None, input_files=None, json_file=None,
                         output_file=None, verbose=0, query=None):
    if not domain_files:
        domain_files = []
    if not fact_files:
        fact_files = []
    if not input_files:
        input_files = []
    if not isinstance(input_files,list):
        input_files = [input_files]

    if not bridge_files:
        bridge_files = []
    if not isinstance(bridge_files,list):
        bridge_files = [bridge_files]

    parser = buildqueryargparser()
    args = []
    if bridge_files:
        args += ["-b"] + bridge_files

    args += ["-d"] + domain_files

    if len(fact_files) > 0:
        args += ["-f"] + fact_files

    args += ["-i"] + input_files

    if json_file is not None:
        args += ["-j", json_file]

    if output_file is not None:
        args += ["-o", output_file]

    if verbose > 0:
        args += ["-{v}".format(v="v" * verbose)]

    if query is not None:
        args += ["-q", query]

    (a, u) = parser.parse_known_args(args)
    return instal_solve_with_args(a, u)

def instal_solve_with_args(args, unk):
    args, unk = check_args(args,unk,query=True)
    return instal_query_with_args(args, unk)

if __name__ == "__main__":
    instal_solve()
