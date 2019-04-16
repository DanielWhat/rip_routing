"""
A rough testing function. Need to change later
"""

from rip_packet import generate_rip_response_packet, is_packet_valid, print_packet_contents
import socket
from Route import Route
import datetime
        
        
#generate some packets

routing_table = dict();

#route_1 = Route(4, 4, 4321, 1, datetime.datetime.now())
#routing_table[4] = route_1

route_2 = Route(4321, 7, 5321, 1, datetime.datetime.now())
routing_table[4321] = route_2

route_3 = Route(4021, 7, 5121, 1, datetime.datetime.now())
routing_table[4021] = route_3

#print(is_packet_valid(generate_rip_response_packet(1232, routing_table, [4, 4321, 4021])))

packet = generate_rip_response_packet(1, 34, routing_table, [4321, 4021])

socket_obj = socket.socket(type=socket.SOCK_DGRAM)

socket_obj.sendto(packet, ('127.0.0.1', 5001))