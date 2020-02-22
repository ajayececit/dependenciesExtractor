import sys
import os
import argparse
import logging
import re

from service import isPython
from service import convertAST
from service import dependenciesServices
from astClass import ASTAnalyser
from exceptions import NotAPythonFile, ArgumentError


astAnalyserObject = ASTAnalyser()
dependenciesClassObject = dependenciesServices()

def extractor(root, name):
    '''Check for the python file and convert the data into ast to get module/library/dependencies 
    used'''
    try:
        if isPython(name):
            filePath = root + "\\" + name
            abstractSyntaxTree, fileData = convertAST(filePath)
            if abstractSyntaxTree:
                astAnalyserObject.visit(abstractSyntaxTree)
                astAnalyserObject.getData(abstractSyntaxTree)
                dependencies = astAnalyserObject.getDependencies()
                duplicateDependencies = astAnalyserObject.getDuplicateDependencies()    
                usedVariables = astAnalyserObject.getCollections("variable")
                usedMethods = astAnalyserObject.getCollections("method")
                totalVariablesUsed = len(usedVariables)
            # call file write func here
            dependenciesLineNumber = astAnalyserObject.getLineNumbers()
            dependenciesClassObject.dependenciesList(dependenciesLineNumber, fileData, name)
            # print(dependencies)
            # print(duplicateDependencies)
            # print(usedVariables, totalVariablesUsed)    
            # print(usedMethods)
        else:
            raise NotAPythonFile
    except NotAPythonFile as e:
        print("{} is not a python file".format(name))

def iterateFolder():
    ''' Iterate through all folder and subfolder for all the python files'''
    for root, _, files in os.walk(args.folder):
        for name in files:
            extractor(root, name)

        dependenciesClassObject.dependenciesWriter(root)
        dependenciesClassObject.dependenciesMapper(root)
        dependencies = astAnalyserObject.getDependencies()
        dependenciesClassObject.usedDependencies(root, dependencies)


def iterateFile(filePath):
    '''Open and check for the libraries used in the given file'''
    root = os.path.dirname(filePath)
    name = os.path.basename(filePath) 
    extractor(root, name)
    dependenciesClassObject.dependenciesWriter(root)
    dependenciesClassObject.dependenciesMapper(root)

def main(args):
    if sys.version_info[0]==2:
        # For further development
        pass

    elif sys.version_info[0]==3:
        try:
            if args.folder and args.file:
                raise ArgumentError

            if args.folder:
                iterateFolder()
            elif args.file:
                iterateFile(args.file)
            elif args.find:
                # finding a particular module in a folder or file function should goes here
                pass
            else:
                print("Warning reading from root file")
        except ArgumentError:
            print("cannot provide both --folder and --file argument")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract Python Dependencies.')
    parser.add_argument('--file',
                        help='provide the folder path of python files')
    parser.add_argument('--folder',
                        help='provide the folder path of python files')
    parser.add_argument('--find',
                        help='provide the library need to find in files')

    args = parser.parse_args()
    main(args)