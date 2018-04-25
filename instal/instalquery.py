if __name__ == "__main__":
    raise NotImplementedError("Try running ../instalquery.py instead.")

from io import StringIO
from typing import List, IO, Optional

from .clingo import Symbol, parse_term

from instal import InstalFile

from .instalargparse import buildqueryargparser, check_args, getqueryargs
from .models.InstalMultiShotModel import InstalMultiShotModel


def instal_query_with_args(args, unk):
    args, unk = check_args(args,unk,query=True)
    ial_files = [open(f, "rt") for f in args.ial_files]
    bridge_files = [open(f,"rt") for f in args.bridge_files]
    lp_files = [open(f,"rt") for f in args.lp_files]
    domain_files = [open(f, "rt") for f in args.domain_files]
    fact_files = [open(f,"rt") for f in args.fact_files]
    query_file = open(args.query,"rt") if args.query else None
    json_file = args.json_file if args.json_file else None

    return instal_query_files(ial_files=ial_files,bridge_files=bridge_files,
                              lp_files=lp_files,domain_files=domain_files,
                              fact_files=fact_files,query_file=query_file,
                                        json_file=json_file,
                                        verbose=args.verbose,answerset=args.answer_set,
                                        length=args.length,number=args.number)


def instal_query_keyword(bridge_files=None, domain_files=None, fact_files=None, input_files=None, json_file=None,
                         output_file=None, verbose=0, query=None, number=1, length=0, answerset=0):
    if not domain_files:
        domain_files = []
    if not fact_files:
        fact_files = []
    if not input_files:
        input_files = []
    if not bridge_files:
        bridge_files = []
    parser = buildqueryargparser()
    args = []

    if bridge_files:
        args += ["-b"] + bridge_files

    if domain_files:
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

    # ...Okay, for some reason this only works if I pass it the str of length. Why?
    args += ["-l", str(length)]
    args += ["-n", str(number)]
    args += ["-a", answerset]
    (a, u) = parser.parse_known_args(args)
    return instal_query_with_args(a, u)

def instal_query_files(ial_files : List[InstalFile], bridge_files : List[InstalFile] = None, lp_files : List[InstalFile] = None,
        domain_files : List[InstalFile] = None, fact_files : List[InstalFile] = None, query_file : Optional[InstalFile] = None,
        json_file : Optional[str] = None, verbose : int = 0, answerset : int = 0, length : int = 0, number : int = 1):
    if not ial_files: ial_files = []
    if not bridge_files: bridge_files = []
    if not lp_files: lp_files = []
    if not domain_files: domain_files = []
    if not fact_files: fact_files = []
    query_text = query_file.read() if query_file else ""
    query_events = [] # type: List[Symbol]
    for q in StringIO(query_text):
        query_events.append(parse_term(q))

    if length == 0 and query_events:
        length = len(query_events)

    if length == 0:
        length = 1

    model = InstalMultiShotModel(ial_files=ial_files,bridge_files=bridge_files,lp_files=lp_files,domain_files=domain_files,
                                 fact_files=fact_files,verbose=verbose,answer_set=answerset,length=length,number=number)
    answersets = model.solve(query_events)
    model.check_and_output_json(json_file)
    return answersets


def instal_query():
    args, unk = getqueryargs()
    return instal_query_with_args(args, unk)
