"""
Main.py, authors: jbr185, 66360439 and dwa110, 28749539

The main entry point for the program/daemon
"""

from MyUtils import getCommandLineArgument
from FileReader import readConfig
import routing_table 
import select
from rip_timer import start_background_timers
from rip_sockets import generate_sockets
from sys import exit, argv

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



class Router(object):
    def __init__(self, routing_table, router_id, input_ports, output_links):
        self.routing_table = routing_table
        self.router_id = router_id
        self.input_ports = input_ports
        self.output_links = output_links
        self.next_periodic_update = None
        self.next_triggered_update = None
        self.triggered_update_routes = []


def main():
    filename = argv[1]
    
    #get directly connected routing info
    own_router_id, input_ports, output_links = readConfig(filename)
    router = Router(dict(), own_router_id, input_ports, output_links)
    
    #configure input sockets
    socket_list = generate_sockets(router.input_ports)
    socket_fd_list = [socket_obj.fileno() for socket_obj in socket_list]
    socket_dict = {socket_obj.fileno(): socket_obj for socket_obj in socket_list}
    
    routing_table.initialise_routing_table(router.routing_table, router.output_links)
    
    #start background processes/timer
    start_background_timers(router) #@@@ when an exception occurs this timer needs to be stopped as well
    
    print("*" * 10, "Initial Routing Table", "*" * 10)
    for key in router.routing_table.keys():
        print(router.routing_table[key])
        print("")
    
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
            
            #send the packet away to be processed
            routing_table.process_packet(router, request_packet)
            
            #print routing table
            print("Update received from socket {}".format(address[1]))
            print("*" * 10, "Routing Table", "*" * 10)
            for key in router.routing_table.keys():
                print(router.routing_table[key])
                print("")
        
        

if __name__ == '__main__':
    main()
        
    
