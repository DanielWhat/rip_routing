"""
rip_packet.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import socket
from sys import exit

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


#print(generate_sockets([1234, 1235, 1236]))
            