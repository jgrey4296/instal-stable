
class InstalBaseASTVisitor:
    """
    A Base AST Visitor
    to generate visitor methods onto using
    instal.util.genetate_visitors
    """

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
