import re
import ast
import logging
import os

''' Module which will provide the required service for the application '''
def isPython(filename):
    if filename.endswith((".txt", ".py")):
        return True
    else:
        try:
            file_head = open(filename).read(64)
            if re.match("#!.*\\bpython", file_head):
                return True
        except IOError:
            return False


def isModule(filename):
    if filename.match("__init__.py"):
        return True


def convertAST(filePath):
    '''Function to convert the file data to Abstract Syntax Tree'''
    with open(filePath, "r") as pyFile:
        try:
            fileContent = pyFile.read()
            fileData = fileContent.splitlines()
            abstractSyntaxTree = ast.parse(fileContent)
        except SyntaxError as e:
            print("***{}*** ERROR in the {} line of {} file" .format(e.msg, e.lineno, filePath))
            #error = '%s:%s: %s' % (pyFile, err.lineno or '--', err.msg)
            return None
        except TypeError as e:
            print("***{}*** ERROR in the {} line of {} file" .format(e, e, filePath))
            #error = '%s:%s: %s' % (pyFile, err.lineno or '--', err.msg)
            return None
    return abstractSyntaxTree, fileData


class dependenciesServices:
    def __init__(self):
        self.importStatement = []
        self.importMaper = []


    def dependenciesList(self, lineNumber, fileData, fileName):
        lineNumber = list(set(map(lambda i: tuple(sorted(i)), lineNumber))) 
        for startEnd in lineNumber:
            if startEnd[0] == startEnd[1]:
                importStatement = fileData[startEnd[0]-1].strip()
                importMaper = importStatement + "--" + str(startEnd[0]) + "--" + fileName
            else:
                importStatement = ""
                for line in range(startEnd[0], startEnd[1]+ 1):
                    importStatement = importStatement + fileData[line-1].strip().replace("\\", "")
                importMaper = importStatement + "--" + str(startEnd[0]) + "--" + fileName
            self.importMaper.append(importMaper)
            self.importStatement.append(importStatement)

    
    def getimportMaperList(self):
        return self.importMaper


    def getImportList(self):    
        return self.importStatement


    def removeDuplicateLibrary(self, listToRemove):
        self.importStatement = list(set(listToRemove))
        return self.importStatement


    def dependenciesWriter(self, root):
        path = os.path.join(root, "output")
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "\\" + "dependencies_list.txt", 'w') as out_file:
            for lines in self.removeDuplicateLibrary(self.getImportList()):
                out_file.write(lines + "\n")

    
    def dependenciesMapper(self, root):
        path = os.path.join(root, "output")
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "\\" + "import_maper.txt", 'w') as out_file:
            for lines in self.removeDuplicateLibrary(self.getimportMaperList()):
                out_file.write(lines + "\n")


    
    def usedDependencies(self, root, dependencies):
        path = os.path.join(root, "output")
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "\\" + "used_dependencies.txt", 'w') as out_file:
            for lines in dependencies['import']:
                out_file.write(lines + "\n")
            for lines in dependencies['from']:
                out_file.write(lines + "\n")

    
    def usedFunctionandMethon(self):
        # to print the used function and method here
        pass




