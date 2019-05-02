"""
rip_packet.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import socket
from sys import exit
from rip_packet import generate_rip_response_packet 

def generate_sockets(input_ports):
    """
    Takes a list of input port numbers, and creates a list of sockets with each 
    socket binded to a respective port number. Input port numbers must be a 
    a unique list (i.e no duplicate port numbers)
    """
    socket_list = []
    
    for i, port_num in enumerate(input_ports):
        #try open all the sockets
        try:
            socket_list.append(socket.socket(type=socket.SOCK_DGRAM))
        
        except Exception as error:
            ##close all the previously opened sockets
            for j in range(i-1, -1, -1):
                socket_obj = socket_list[j]
                socket_obj.close()
            print("While opening sockets the following error was encountered:")
            print(error)
            exit()
            
        #try bind all the sockets
        try:
            socket_list[i].bind(('127.0.0.1', port_num)) #this function will raise an exeption on duplicate port nums
            
        except Exception as error:
            #close all the previously opened sockets
            for j in range(i, -1, -1): #now i instead of i-1 because we must close the socket opened in the try except block above
                socket_obj = socket_list[j]
                socket_obj.close()            
            print("While binding a socket to the port number {} the following error was encountered:".format(port_num))
            print(error)
            exit()
            
    return socket_list



def send_routes_to_neighbours(router, route_ids_to_send, is_triggered_update=False):
    """
    Takes a router object, routing_table, and a list of router IDs to send. And 
    sends an update packet to all neighbours with the routes to each router in
    the list of router IDs.
    """
    if is_triggered_update:
        router.next_triggered_update = None #we are just about to send the triggered update, so there is no next triggered update now
    
    #create socket from where we will be sending --- this is probably bad practice @@@
    try:
        socket_obj = socket.socket(type=socket.SOCK_DGRAM)
        
    except Exception as error:
        print("The following exception occured when trying to open a socket:")
        print(error)
        print("")
        print("*" * 10, "SINCE SOCKET COULD NOT BE OPENED UPDATE WILL BE SKIPPED.", "*" * 10)
        #no need to close socket if it could not be created to begin with
    
    #if no exception occurs then proceed with the following    
    else:
        neighbouring_router_links = [link for link in router.output_links]

        #send an update to each neighbouring router
        for neighbouring_router_link in neighbouring_router_links:
            packet = generate_rip_response_packet(router.router_id, neighbouring_router_link.routerID, router.routing_table, route_ids_to_send) #create the packet 
            
            try:
                #print(packet)
                socket_obj.sendto(packet, ('127.0.0.1', neighbouring_router_link.port)) #send the packet
            except Exception as error:
                print("The following exception occured when trying to open a socket. The update packet to router {} has been skipped.".format(neighbouring_router_link.routerID))
                print(error)
                print("") 
                
    finally: #code here is executed regardless of any exceptions 
        socket_obj.close()    


#print(generate_sockets([1234, 1235, 1236]))
            