import re
from re import compile
import inspect
import os

ALL_NODES = dict()

class Node():
    def __init__(self, name=None, location = [0,0], *args, **kwargs):
        self.type = "Node"
        self.name = name
        self.location = location


class FileNode(Node):
    def __init__(self, filename=None, filePath = Node, **kwargs):
        if "name" not in kwargs.keys():
            kwargs["name"] = filename
        super().__init__(**kwargs)
        self.type = "File"
        self.filename = filename
        self.filePath = filePath


class PythonNode(FileNode):
    def __init__(self, eval = False, **kwargs):
        super().__init__(**kwargs)
        self.type = "Python"

        if "depth" in kwargs:
            self.recursionDepth = kwargs["depth"]
        else:
            self.recursionDepth = 0

        self.importSearch = re.compile(r".*?(import|from)\s(.*?)\s")
        
        self.imports = dict()
        self.functions = []
        self.publicFunctions = []
        if eval:
            self.evaluate()

    def evaluate(self, recusive = None):
        #read the file
        with open(self.filename) as f:
            self.rawFile = f.readlines()
        if self.recursionDepth < 3:
            self.findImports()

    def findImports(self):
        self.imports = dict()
        for line in self.rawFile:
            results = self.importSearch.match(line)
            if results:
                importName = results.group(2)
                self.imports[importName] = None

                if importName in ALL_NODES:
                    self.imports[importName] = ALL_NODES[importName]
                else:
                    for importName in self.imports.keys():
                        try:
                            #import it
                            exec("import " + importName)

                            #find its path
                            importPath = eval(importName + ".__file__")

                            #un-import it
                            exec("del(" + importName + ")")

                            if ".py" in importPath:
                                self.imports[importName] = PythonNode(filename = importPath, name=importName, eval=True, depth=self.recursionDepth+1)
                            else:
                                self.imports[importName] = FileNode(filename = importPath, name=importName)
                        except:
                            try:
                                self.imports[importName] = Node(importName)
                            except:
                                print("ignoring", importName)
                                del(self.imports[importName])
                
    def addConnection(self, source, destination):
        pass

    def printConnections(self, indent=0):
        print("-"*indent + ">" + "[" + str(self.name) + "]")
        for importName in self.imports.keys():
            if self.imports[importName].type == "Python":
                self.imports[importName].printConnections(indent + len(self.name) + 2)
            else:
                print("-"*indent + ">", importName)