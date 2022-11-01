import instal.interfaces.ast as iAST
from dataclasses import InitVar, dataclass, field
from collections import defaultdict
import logging as logmod

from instal.interfaces.util import InstalASTVisitor_i

logging = logmod.getLogger(__name__)

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
    """
    actions : dict[type[iAST.InstalAST], set[callable]] = field(default_factory=lambda: defaultdict(set))

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
        try:
            result = visitor(node)
        except Exception as err:
            logging.exception("Visit attempt failed: %s : %s", visitor, node)

        return result


    def generic_visit(self, node):
        logging.info("Generic Visit Called, doing nothing: %s", node)

    def visit_all(self, nodes:list[iAST.InstalAST]):
        for x in nodes:
            self.visit(x)
