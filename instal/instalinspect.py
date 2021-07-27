from io import StringIO
from typing import List, IO, Optional

from clingo import Symbol, parse_term

from instal import InstalFile

from .instalargparse import buildqueryargparser, check_args, getqueryargs
from .models.InstalDummyModel import InstalDummyModel

def instal_inspect_with_args(args, unk):
    args, unk = check_args(args,unk,query=True)
    ial_files = [open(f, "rt") for f in args.ial_files]
    bridge_files = [open(f,"rt") for f in args.bridge_files]
    lp_files = [open(f,"rt") for f in args.lp_files]
    domain_files = [open(f, "rt") for f in args.domain_files]
    fact_files = [open(f,"rt") for f in args.fact_files]
    query_file = open(args.query,"rt") if args.query else None
    json_file = args.json_file if args.json_file else None

    return instal_inspect_files(ial_files=ial_files,bridge_files=bridge_files,
                              lp_files=lp_files,domain_files=domain_files,
                              fact_files=fact_files,query_file=query_file,
                                        json_file=json_file,
                                        verbose=args.verbose,answerset=args.answer_set,
                                        length=args.length,number=args.number)

def instal_inspect_files(ial_files : List[InstalFile], bridge_files : List[InstalFile] = None, lp_files : List[InstalFile] = None,
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

    model = InstalDummyModel(ial_files=ial_files,bridge_files=bridge_files,lp_files=lp_files,domain_files=domain_files,
                                 fact_files=fact_files,verbose=verbose,answer_set=answerset,length=length,number=number)
    declarations = model.get_declarations()
    if verbose > 0:
        print("Inspection profile:")
        print(declarations)
    # TODO Should this dump to json as defined by thing, or?
    return declarations

def instal_inspect():
    args, unk = getqueryargs()
    return instal_inspect_with_args(args, unk)
