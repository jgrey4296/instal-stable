import instal.interfaces.ast as iAST

class InstalBaseASTVisitor:
    """
    A Base AST Visitor
    to generate visitor methods onto using
    instal.util.generate_visitors

    Based off of python stdlib: ast.NodeVisitor
    """

    def visit(self, node):
        """Visit a node."""
        assert(isinstance(node, iAST.InstalAST))
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        logging.info("Generic Visit Called, doing nothing: %s", node)
