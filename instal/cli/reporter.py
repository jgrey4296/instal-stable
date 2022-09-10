#! /usr/bin/env python
"""
CLI program to load instal trace JSONs and create different output formats of them

"""
##-- imports
from __future__ import annotations

import argparse
import json
import logging as logmod
import os
import pathlib
from sys import stderr, stdout

from instal.report.gantt import InstalGanttReporter
from instal.report.pdf import InstalPDFReporter
from instal.report.text import InstalTextReporter
from instal.trace.trace import InstalTrace
from instal.util.misc import InstalOptionGroup

##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

##-- argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target',      help="Specify (multiple) files and directories to load", required=True)
parser.add_argument("-o", "--output",      type=str, help="output dir location, defaults to {cwd}/instal_tmp")
parser.add_argument("-v", "--verbose", action='count', help="turns on trace output, v for holdsat, vv for more")
parser.add_argument("-g", "--gantt",   action="store_true", help="specify output file for gantt visualization")
parser.add_argument("-x", "--text",    action="store_true", help="specify output file for text trace")
parser.add_argument("-p", "--pdf",    action="store_true", help="specify output file for pdf trace")
##-- end argparse

def main():
    ##-- Logging
    DISPLAY_LEVEL = logmod.DEBUG
    LOG_FILE_NAME = "log.{}".format(pathlib.Path(__file__).stem)
    LOG_FORMAT    = "%(asctime)s | %(levelname)8s | %(message)s"
    FILE_MODE     = "w"
    STREAM_TARGET = stdout

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

    args = parser.parse_args()
    trace_path = pathlib.Path(args.target).expanduser().resolve()
    assert(trace_path.exists())
    assert(trace_path.suffix == ".json")

    option_group = InstalOptionGroup(verbose=args.verbose,
                                     output=pathlib.Path(args.output if args.output else "instal_tmp").expanduser().resolve(),
                                     )
    logging.setLevel(option_group.loglevel)

    logging.info("Loading Trace: %s", trace_path)
    trace = InstalTrace.from_json(json.loads(trace_path.read_text()))

    if args.gantt:
        logging.info("Building Gantt Report")
        instal_gantt_reporter = InstalGanttReporter()
        instal_gantt_reporter.trace_to_file(trace, option_group.output / "gantt_report.tex")

    if args.pdf:
        logging.info("Building Pdf Report")
        instal_pdf_reporter = InstalPDFReporter()
        instal_pdf_reporter.trace_to_file(trace, option_group.output / "pdf_report.tex")

    if args.text or not (args.gantt or args.pdf):
        logging.info("Building Text Report")
        instal_text_reporter = InstalTextReporter()
        instal_text_reporter.trace_to_file(trace, option_group.output / "text_report.txt")


if __name__ == "__main__":
    main()
