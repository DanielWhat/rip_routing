"""
Main.py, authors: jbr185, 66360439 and dwa110, 28749539

The main entry point for the program/daemon
"""
from MyUtils import getCommandLineArgument
from FileReader import readConfig
import routing_table
import select
from rip_sockets import generate_sockets
from sys import exit

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
    rip_routing_table = dict()
    #get directly connected routing into
    routerID, input_ports, output_links = readConfig("test.txt")
    
    #configure input sockets
    socket_list = generate_sockets(input_ports)
    socket_fd_list = [socket_obj.fileno() for socket_obj in socket_list]
    socket_dict = {socket_obj.fileno(): socket_obj for socket_obj in socket_list}
    
    routing_table.initialise_routing_table(rip_routing_table, output_links)
    #start timeout expiry process here @@@
    
    # ************ ENTER INFINITE SELECT LOOP ************
    while True:
        #listen for incoming packets  
        try:
            ready_sockets = select.select(socket_fd_list, [], [])
        
        except Exception as error:
            #close all sockets
            for i in range(len(socket_list)):
                socket_list[i].close()
            print("The following error was encountered when using the select() command.")
            print(error)
            exit()
            
        for socket_fd in ready_sockets[0]:
            
            #receive packets
            try:
                request_packet, address = socket_dict[socket_fd].recvfrom(4096)
                
            except Exception as error:
                #close all sockets
                for i in range(len(socket_list)):
                    socket_list[i].close()
                print("The following error was encountered when trying to read data from the socket with file descriptor {}".format(socket_fd))
                print(error)
                exit()       
            
            #here we would send the packet away for processing @@@    
            print(request_packet)

main()
