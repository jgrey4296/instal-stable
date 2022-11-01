#/usr/bin/env python3
"""

"""
##-- imports
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

import instal.interfaces.ast as iAST

from instal.interfaces.util import InstalASTVisitor_i
if TYPE_CHECKING:
    # tc only imports
    pass
##-- end imports

##-- logging
logging = logmod.getLogger(__name__)
# If CLI:
# logging = logmod.root
# logging.setLevel(logmod.NOTSET)
##-- end logging

@dataclass
class InstalBaseASTVisitor(InstalASTVisitor_i):
    """
    A Base AST Visitor
    to generate visitor methods onto using
    instal.cli.generate_visitors

    Based off of python stdlib: ast.NodeVisitor

    visitor.actions is a dict mapping classes -> set[functions] to run on a node.
    __post_init__ flattens these sets so parent class actions are added to subclass entries
    to avoid going up the mro list on visitor.visit

    if an action is *just* for a class, and not its children, add it *after* visitor construction

    actions are expected to have the signature func(visitor, node) -> None

    actions are called *before* visiting children
    """

    actions : dict[type[iAST.InstalAST], set[callable]] = field(default_factory=lambda: defaultdict(set))

    current_path : list[iAST.InstalAST] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.flatten()

    def add_actions(self, a_dict):
        """
        add visit actions to the visitor,
        the dict of actions being: dict[classType -> set[callable]]
        """
        assert(isinstance(a_dict, dict))
        for key, act_set in a_dict.items():
            self.actions[key].update(act_set)

    def flatten(self):
        # flatten action lists to avoid having to look up mro orders in visit
        for key in self.actions.keys():
            for mro_entry in key.__mro__:
                mro_actions = self.actions.get(mro_entry) or []
                self.actions[key].update(mro_actions)


    def visit(self, node, *, skip_actions=False):
        """Visit a node."""
        assert isinstance(node, iAST.InstalAST)
        self.current_path.append(node)
        logging.debug("Entering Visit: %s", node)
        if not skip_actions:
            actions = self.actions.get(node.__class__) or []
            logging.debug("Running %s actions", len(actions))
            for func in actions:
                try:
                    func(self, node)
                except Exception as err:
                    logging.exception("Visit Action Failed: %s : %s", func, node)

        logging.debug("Running visit")
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        result  = None
        try:
            result = visitor(node)
        except Exception as err:
            logging.exception("Visit attempt failed: %s : %s", visitor, node)

        assert(self.current_path[-1] is node)
        self.current_path.pop()
        return result

    def generic_visit(self, node):
        logging.info('Generic Visit Called, doing nothing: %s', node)

    def visit_all(self, nodes: list[iAST.InstalAST]):
        for x in nodes:
            self.visit(x)

    def visit_BridgeDefAST(self, node):
        self.visit_InstitutionDefAST(node)
        self.visit_all(node.connections)

    def visit_ConditionAST(self, node):
        self.visit(node.head)
        if node.rhs is not None:
            self.visit(node.rhs)

    def visit_DomainSpecAST(self, node):
        self.visit(node.head)
        self.visit_all(node.body)

    def visit_EventAST(self, node):
        self.visit(node.head)

    def visit_FluentAST(self, node):
        self.visit(node.head)

    def visit_GenerationRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_InertialRuleAST(self, node):
        self.visit_RuleAST(node)

    def visit_InitiallyAST(self, node):
        self.visit_all(node.body + node.conditions)

    def visit_InstalAST(self, node):
        raise TypeError("InstalAST's should be abstract")

    def visit_InstitutionDefAST(self, node):
        self.visit(node.head)
        self.visit_all(node.fluents
                       + node.events
                       + node.types
                       + node.rules
                       + node.initial)

    def visit_QueryAST(self, node):
        self.visit(node.head)
        self.visit_all(node.conditions)


    def visit_RuleAST(self, node):
        self.visit(node.head)
        self.visit_all(node.body + node.conditions)

    def visit_BridgeLinkAST(self, node):
        self.visit(node.head)

    def visit_TermAST(self, node):
        self.visit_all(node.params)

    def visit_TransientRuleAST(self, node):
        self.visit_RuleAST(node)

