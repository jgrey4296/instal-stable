#! /usr/bin/env python
##-- imports
from __future__ import annotations

import logging as logmod
import pathlib
import time
from sys import stderr, stdout
from typing import List, Optional

import requests
import simplejson as json
from instal.defaults import INSTAL_API
from instal.parser.domainparser import DomainParser
##-- end imports

##-- Logging
DISPLAY_LEVEL = logmod.DEBUG
LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
FILE_MODE     = "w"
STREAM_TARGET = stderr # or stdout

logger          = logmod.getLogger(__name__)
console_handler = logmod.StreamHandler(STREAM_TARGET)
file_handler    = logmod.FileHandler(LOG_FILE_NAME, mode=FILE_MODE)

console_handler.setLevel(DISPLAY_LEVEL)
# console_handler.setFormatter(logmod.Formatter(LOG_FORMAT))
file_handler.setLevel(logmod.DEBUG)
# file_handler.setFormatter(logmod.Formatter(LOG_FORMAT))

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logging = logger
##-- end Logging

##-- argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('--dir',               type=str, help="Specify a directory to load")
argparser.add_argument('-f', '--file',        action="append", help="Specify (multiple) specific files to load")
argparser.add_argument("-q", "--query",       type=str, help="specify query file (.iaq) - use \"-\" to take from stdin.")

argparser.add_argument("-o", "--output-file", type=str, help="output file/directory for one/several inputs: uses /tmp if omitted")
argparser.add_argument("-j", "--json-file",   type=str, help="specify json output file or directory")

argparser.add_argument("-v", "--verbose",     action='count', help="turns on trace output, v for holdsat, vv for more")
argparser.add_argument('-a', '--answer-set',  type=int, default=0, help='choose an answer set (default all)')
argparser.add_argument('-n', '--number',      type=int, default=1, help='compute at most <n> models (default 1, 0 for all)')
argparser.add_argument('-l', '--length',      type=int, default=0, help='length of trace (default 1)')
##-- end argparse


def instal_remote():
    args = argparser.parse_args()

    file_group   = InstalFileGroup(args)
    option_group = InstalOptionGroup(verbose=args.verbose,
                                     answer_set=args.answer_set,
                                     length=args.length,
                                     number=args.number)

    return instal_remote_files(file_group, option_group)


def instal_remote_files(filegroup:InstalFileGroup, optgroup:InstalOptionGroup):

    old_types    = DomainParser.DomainParser().get_groundings(filegroup.domains)
    types        = {}

    for k, v in old_types.items():
        types[k] = list(v)
    q = [l.replace("\n","")[9:][:-1] for l in query_file] if query_file else []

    response = requests.post(INSTAL_API + "/new/",
                             data=json.dumps(
                                 {"institutions" : [i.read() for i in ial_files],
                                  "bridges"      : [b.read() for b in bridge_files],
                                  "types"        : types,
                                  "length"       : length,
                                  "facts"        : [f.read() for f in fact_files],
                                  "query"        : q,
                                  "number"       : number}
                             ),
                             headers={'Content-Type': 'application/json'})

    assert(response.status_code==201)
    json_resp = response.json()
    model_id, grounding_id, query_id = (json_resp.get("grounding", {}).get("model", {}).get("id"),
                                        json_resp.get("grounding", {}).get("id"),
                                        json_resp.get("id"))

    logging.info("Successful send. Processing...")
    n = 30
    status = ""
    while n > 0:
        response = requests.get(INSTAL_API + f"/model/{model_id}/grounding/{grounding_id}/query/{query_id}/",
                                headers={'Accept': 'application/json'})

        if (response.status_code == 200):
            status = response.json().get("status")
            if status == "error" or status == "complete":
                break
        n -= 1
        time.sleep(0.1)

    match status:
        case "complete:"
            json_resp = response.json()
            logging.info("Complete")
            n_answersets = json_resp.get("n_answer_sets",1)
            logging.info("Number of answersets: {}".format(n_answersets))
            answer_set_id = 0

            if optgroup.verbose:
                if n_answersets == 1:
                    answer_set_id = 1
                while not ((answer_set_id == "all") or (int(answer_set_id) >= 1 and int(answer_set_id) <= n_answersets)):
                    answer_set_id = input("Please enter the number of the answer set you want to see the text output for (1-{}, all): ".format(n_answersets))
                if answer_set_id == "all":
                    for answer_set_id in range(1,n_answersets+1):
                        print_text_for(model_id, grounding_id, query_id, answer_set_id)
                else:
                    print_text_for(model_id,grounding_id,query_id,answer_set_id)

            if optgroup.json_out:
                if n_answersets == 1:
                    answer_set_id = 1
                while not ((answer_set_id == "all") or (int(answer_set_id) >= 1 and int(answer_set_id) <= n_answersets)):
                    answer_set_id = input("Please enter the number of the answer set you want to save the json output for (1-{}, all): ".format(n_answersets))
                if answer_set_id == "all":
                    for answer_set_id in range(1,n_answersets+1):
                        j = get_json_for(model_id,grounding_id,query_id,answer_set_id)
                        dump_json_to_file(j,"{}_{}".format(answer_set_id,json_file))
                else:
                    j = get_json_for(model_id, grounding_id, query_id, answer_set_id)
                    dump_json_to_file(j,json_file)
        case "error":
            logging.error("Error")
            json_resp = response.json()
            error, message = json_resp.get("errors")[0], json_resp.get("errors")[1]
            logging.error(error)
            logging.error(message)
            return
        case _:
            logging.warning("Failed to complete in time.")
            return

def print_text_for(model_id,grounding_id,query_id,answer_set_id):
    response = requests.get(INSTAL_API + f"/model/{model_id}/grounding/{groundind_id}/query/{query_id}/output/{answer_set_id}/",
                            headers={"Accept": "text/plain"})
    assert (response.status_code == 200)
    logging.info(response.text)

def get_json_for(model_id,grounding_id,query_id,answer_set_id):
    response = requests.get(INSTAL_API + f"/model/{model_id}/grounding/{grounding_id}/query/{query_id}/output/{answer_set_id}/",
                            headers={"Accept": "application/json"})
    assert (response.status_code == 200)
    return response.json()


if __name__ == "__main__":
    instal_remote()

