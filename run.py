


if __name__ == "__main__":
    print("Running")
    print("Creating a Node")
    from nodes import * 

    newnode = PythonNode(filename = "run.py")

    newnode.evaluate()

    newnode.printConnections()