import ast

class ASTAnalyser(ast.NodeVisitor):

    def __init__(self):
        self.dependencies = {"import" : [], "from" : []}
        self.duplicateDependencies = {"import" : [], "from" : []}
        self.collections = {"variable" : [], "method" : [], "attribute" : []}
        self.lineNumber = []


    def visit_Import(self, node):
        for alias in node.names:
            if alias.name is not '__future__':
                if alias.name not in self.dependencies["import"]:
                    self.dependencies["import"].append(alias.name)
                    self.lineNumber.append([node.lineno, node.end_lineno])
                else:
                    self.duplicateDependencies["import"].append(alias.name)
            self.generic_visit(node)


    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name not in self.dependencies["from"]:
                self.dependencies["from"].append(alias.name)
                self.lineNumber.append([node.lineno, node.end_lineno])
            else:
                self.duplicateDependencies["from"].append(alias.name)
        self.generic_visit(node)


    def getData(self, root):
        for node in ast.walk(root):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                self.collections["variable"].append(node.id)
            elif isinstance(node, ast.Attribute):
                self.collections["attribute"].append(node.attr)
            elif isinstance(node, ast.FunctionDef):
                self.collections["method"].append(node.name)

    
    def getDependencies(self):
        return self.dependencies
    

    def getDuplicateDependencies(self):
        return self.duplicateDependencies


    def getCollections(self, data):
        return self.collections[data]


    def getLineNumbers(self):
        lineNumberList = self.lineNumber
        self.lineNumber = []
        return lineNumberList

