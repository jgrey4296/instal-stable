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

    actions : dict[str, set[callable]] = field(default_factory=lambda: defaultdict(set))

    current_path : list[iAST.InstalAST] = field(init=False, default_factory=list)

    def add_actions(self, actions_obj:Any):
        """
        add visit actions to the visitor,
        any methods on the object of the form action_{CLASSNAME}
        will be recorded
        """
        for action in dir(actions_obj):
            a_match = ACTION_RE.match(action)
            if a_match:
                self.actions[a_match[1]].add(getattr(actions_obj, action))

    def flatten_for_classes(self, *classes):
        """ flatten action sets to avoid having to look up mro order repeatedly"""
        if not classes and hasattr(iAST, '__all__'):
            classes = [getattr(iAST, x) for x in iAST.__all__
                       if issubclass(getattr(iAST, x), iAST.InstalAST)]

        for cls in classes:
            logging.debug("Flattening: %s : %s", cls.__name__, cls.__mro__)
            for mro in cls.__mro__:
                mro_actions = self.actions.get(mro.__name__) or []
                self.actions[cls.__name__].update(mro_actions)

    def visit(self, node, *, skip_actions=False):
        """Visit a node."""
        assert isinstance(node, iAST.InstalAST)
        self.current_path.append(node)
        logging.debug("Entering Visit: %s", node)
        if not skip_actions:
            actions = self.actions.get(node.__class__.__name__) or []
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
        logging.info("Generic Visit Called, doing nothing: %s", node)

    def visit_all(self, nodes:list[iAST.InstalAST]):
        for x in nodes:
            self.visit(x)
