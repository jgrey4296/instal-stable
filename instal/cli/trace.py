#! /usr/bin/env python
"""
CLI program to load instal trace JSONs and create different output formats of them

"""
##-- imports
from __future__ import annotations

import logging as logmod
import os
import pathlib
from sys import stderr, stdout

from instal.trace.InstalStateTrace import InstalStateTrace
from instal.report.InstalGanttTracer import InstalGanttTracer
from instal.report.InstalPDFTracer import InstalPDFTracer
from instal.report.InstalTextTracer import InstalTextTracer
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
argparser.add_argument('-t', '--target',      action="append", help="Specify (multiple) files and directories to load")
argparser.add_argument("-o", "--output",      type=str, help="output dir location, defaults to {cwd}/instal_tmp")
argparser.add_argument("-v", "--verbose", action='count', help="turns on trace output, v for holdsat, vv for more")
argparser.add_argument("-g", "--gantt",   action="store_true", help="specify output file for gantt visualization")
argparser.add_argument("-x", "--text",    action="store_true", help="specify output file for text trace")
argparser.add_argument("-j", "--json",    action="store_true", help="specify json output file")
##-- end argparse


def instal_trace():
    argparser = argparser.parse_args()

    file_group   = InstalFileGroup(args)
    option_group = InstalOptionGroup(verbose=args.verbose,
                                     answer_set=args.answer_set,
                                     length=args.length,
                                     number=args.number)

    if option_group.gantt_out:
        instal_gantt_tracer = InstalGanttTracer(trace, gantt_file)
        instal_gantt_tracer.trace_to_file()

    if option_group.text_out:
        instal_text_tracer = InstalTextTracer(trace, text_file)
        instal_text_tracer.trace_to_file()

    if option_group.pdf_out:
        instal_pdf_tracer = InstalPDFTracer(trace, pdf_file)
        instal_pdf_tracer.trace_to_file()



if __name__ == "__main__":
    instal_trace()


