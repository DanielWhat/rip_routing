"""
rip_timer.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import threading
import socket
from sys import exit
from rip_packet import generate_rip_response_packet

def rip_update_timer(routing_table, router, output_links):
    """
    A parallel process which sends out automatic routing table updates 
    to neighbouring routers every 30 seconds. Not all routers will receive the 
    same update due to the split horizon with poison reverse rules.
    """
    
    #to minimise delays from computing, start new timer immediately
    timer = threading.Timer(30, rip_update_timer, [routing_table, router, output_links])
    timer.start()
    #@@ will need to do something extra here because the triggered update function needs to know if an periodic update is coming soon
    
    #create socket from where we will be sending --- this is probably bad practice @@@
    try:
        socket_obj = socket.socket(type=socket.SOCK_DGRAM)
        
    except Exception as error:
        print("The following exception occured when trying to open a socket:")
        print(error)
        print("")
        print("*" * 10, "SINCE SOCKET COULD NOT BE OPENED PERIODIC UPDATE WILL BE SKIPPED.", "*" * 10)
        #no need to close socket if it could not be created to begin with
    
    #if no exception occurs then proceed with the following    
    else:
        neighbouring_router_links = [link for link in router.output_links]
        
        #send an update to each neighbouring router
        for neighbouring_router_link in neighbouring_router_links:
            packet = generate_rip_response_packet(router.router_id, neighbouring_router_link.routerID, routing_table, routing_table.keys()) #create the packet 
            
            try:
                print(packet)
                socket_obj.sendto(packet, ('127.0.0.1', neighbouring_router_link.port)) #send the packet
            except Exception as error:
                print("The following exception occured when trying to open a socket. The periodic update packet to router {} has been skipped.".format(neighbouring_router_link.routerID))
                print(error)
                print("")
                
    finally: #code here is executed regardless of any exceptions 
        socket_obj.close()
        
    