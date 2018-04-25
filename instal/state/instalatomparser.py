from typing import List, Tuple

from instal.clingo import Symbol, parse_term

InstalStateListTuple = Tuple[List[Symbol], List[Symbol], List[Symbol]]

from parsec import *

class InstalAtomParser():
    def __init__(self):
        lexeme = lambda p: p << whitespace
        whitespace = regex(r'\s*', re.MULTILINE)
        lbrack = lexeme(string('('))
        rbrack = lexeme(string(')'))
        comma = lexeme(string(','))
        name = lexeme(regex(r'[A-Za-z_][A-Za-z0-9_]*'))
        number = lexeme(regex(r'[0-9]+'))

        @generate
        def atom():
            n = yield name
            ar = yield atomSecondPart
            if not ar: return n
            return [n, ar]

        argPossible = number | atom

        @generate
        def argList():
            elements = yield sepBy(argPossible, comma)
            return elements

        @generate
        def emptyArg():
            yield whitespace
            return []

        atomSecondPart = lbrack >> argList << rbrack | emptyArg

        self.program = atom

    def parse(self, atom):
        return self.program.parse(atom)

    def inverse(self, lst):
        if not isinstance(lst, list): return lst
        if len(lst) == 2 and isinstance(lst[1], list):
            if lst[1]:
                return lst[0] + "(" + self.inverse(lst[1]) + ")"
        return ",".join([self.inverse(a) for a in lst])

instal_atom_parser = InstalAtomParser()

def atom_list_to_str(lst : list) -> str:
    return instal_atom_parser.inverse(lst)

def atom_list_to_symbol(lst : list) -> Symbol:
    return parse_term(atom_list_to_str(lst))

def str_to_atom_list(atomstring : str) -> list:
    return instal_atom_parser.parse(atomstring)

def symbol_to_atom_list(sym : Symbol) -> list:
    return str_to_atom_list(str(sym))

def atom_sorter(y: list) -> list:
    """Returns a list of atoms (i.e. holdsat, occurred, etc)"""
    return sorted(y, key=generate_sorted_lambda, reverse=True
                  )


def generate_sorted_lambda(x: Symbol) -> list:
    criteria = []  # sort by institution name
    if len(x.arguments) > 1:
        criteria.append(x.arguments[1].name)
    fluenttype = x.arguments[0].name
    if fluenttype in ["perm", "pow", "obl", "live", "viol", "tpow", "ipow", "gpow"]:
        criteria.append("")
    else:
        criteria.append(fluenttype)
    criteria.append(fluenttype)
    firstlevel = x.arguments[0].arguments
    if not firstlevel:
        return criteria
    if len(firstlevel) == 0:
        return criteria
    for f in firstlevel:
        criteria.append(f.name)

    secondlevel = firstlevel[0]
    if isinstance(secondlevel, Symbol) or len(secondlevel) == 0:
        return criteria
    for s in secondlevel:
        criteria.append(s.name)
    return criteria