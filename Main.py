"""
Main.py, authors: jbr185, 66360439 and dwa###, ########

The main entry point for the program/daemon
"""
from MyUtils import getCommandLineArgument
from FileReader import readConfig

class Daemon:
    """
    The class for the daemond's operation
    """
    def __init__(self):
        self.routerID = -1
        self.inputs = []
        self.outputs = []

        self.initialize()

    def initialize(self):
        configData = readConfig(getCommandLineArgument(0, str))

        self.routerID = configData[0]
        self.inputs = configData[1]
        self.outputs = configData[2]
    
    def run(self):
        while True:
            continue


def main():
    configData = readConfig("test.txt")
    print("RouterID = {}, Router inputs = {}, router outputs = [{}, {}]".format(configData[0], configData[1], configData[2][0], configData[2][1]))
    return

main()
