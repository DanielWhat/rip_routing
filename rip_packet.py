"""
rip_packet.py, Author: jbr185, 66360439, dwa110, 28749539
"""
import datetime
import Route

RIP_ENTRY_SIZE = 20
RIP_HEADER_SIZE = 4
MAX_NUM_RIP_ENTRIES = 25
RESPONSE_PACKET_COMMAND_NUM = 2
RIP_VERSION_NUM = 2
ADDRESS_FAMILY_IDENTIFIER = 1 #1 is unassigned, so we are using it to indicate router IDs


def get_packet_data(rip_routing_table, packet_bytearray):
  """
  Takes a valid RIP packet and returns the sender's router ID and a list of 
  routes generated from the RIP Entry field.
  """
  list_of_routes = []
  sending_router_id = (packet_bytearray[2] << 8) + packet_bytearray[3]
  
  num_rip_entries = (len(packet_bytearray) - RIP_HEADER_SIZE) // RIP_ENTRY_SIZE
  for i in range(num_rip_entries):
    rip_entry = packet_bytearray[RIP_HEADER_SIZE + i*RIP_ENTRY_SIZE:RIP_HEADER_SIZE + (i+1)*RIP_ENTRY_SIZE]
    
    router_id = (rip_entry[4] << 8*3) + (rip_entry[5] << 8*2) + (rip_entry[6] << 8) + rip_entry[7]
    metric = (rip_entry[16] << 8*3) + (rip_entry[17] << 8*2) + (rip_entry[18] << 8) + rip_entry[19]
    
    #Generate a route object from the RIP entry the router id advertising
    list_of_routes.append(Route.Route(router_id, sending_router_id, rip_routing_table[sending_router_id].gateway_port, min(rip_routing_table[sending_router_id].cost + metric, 16), datetime.datetime.now()))
    
  return sending_router_id, list_of_routes



def is_packet_valid(packet_bytearray):
  """
  Takes a packet and returns true or false respectively depending if the packet 
  is valid. 
  """

  #don't accept if the packet contains less than 1 RIP packet, or more than 25 RIP packets, or rip packet(s) that does/do not contain 20 bytes
  if len(packet_bytearray) < RIP_HEADER_SIZE + RIP_ENTRY_SIZE or len(packet_bytearray) > RIP_HEADER_SIZE + RIP_ENTRY_SIZE * MAX_NUM_RIP_ENTRIES or (len(packet_bytearray) - RIP_HEADER_SIZE) % RIP_ENTRY_SIZE != 0:
    return False
  
  #we only accept response packets
  elif packet_bytearray[0] != RESPONSE_PACKET_COMMAND_NUM:
    return False
  
  #only accept packets with the proper rip version
  elif packet_bytearray[1] != RIP_VERSION_NUM:
    return False
  
  #in the specification this field is 0, but we have put the sending router's ID here instead
  sending_router_id = (packet_bytearray[2] << 8) + packet_bytearray[3]
  if sending_router_id > 64000 or sending_router_id < 1:
    return False
  
  #elif @@ need a statement to reject packets from valid router IDs that are not direct neighbours
  
  num_rip_entries = (len(packet_bytearray) - RIP_HEADER_SIZE) // RIP_ENTRY_SIZE
  for i in range(num_rip_entries):
    rip_entry = packet_bytearray[RIP_HEADER_SIZE + i*RIP_ENTRY_SIZE:RIP_HEADER_SIZE + (i+1)*RIP_ENTRY_SIZE]
    
    #make sure address family identifier is correct
    if rip_entry[0] != 0 or rip_entry[1] != ADDRESS_FAMILY_IDENTIFIER:
      return False
    
    #the next two bytes must be 0 as per the specification
    elif rip_entry[2] != 0 or rip_entry[3] != 0:
      return False
    
    #check that router ID is between 1 and 64000
    router_id = (rip_entry[4] << 8*3) + (rip_entry[5] << 8*2) + (rip_entry[6] << 8) + rip_entry[7]
    if router_id > 64000 or router_id < 1:
      return False
    
    #must be 0 as per the specification
    elif rip_entry[8] != 0 or rip_entry[9] != 0 or rip_entry[10] != 0 or rip_entry[11] != 0:
      return False
    
    #must be 0 as per the specification
    elif rip_entry[12] != 0 or rip_entry[13] != 0 or rip_entry[14] != 0 or rip_entry[15] != 0:
      return False
    
    metric = (rip_entry[16] << 8*3) + (rip_entry[17] << 8*2) + (rip_entry[18] << 8) + rip_entry[19] 
    #the rip metric must be between 1 and 16
    if metric < 1 or metric > 16:
      return False
    
  #if none of the above conditions are true, then the packet is valid
  return True



def generate_rip_response_packet(own_router_id, routing_table, router_id_keys):
  """
  Takes a routing table (a dictionary with router IDs as keys) and a list of 
  router IDs. Returns a RIP packet in the form of a bytearray.
  """
  num_rip_entries = len(router_id_keys)
  
  if num_rip_entries == 0:
    raise ValueError("The list of router IDs cannot be empty.")
  
  elif num_rip_entries > 25:
    raise ValueError("The number of routes in a RIP packet cannot exceed 25.")
  
  packet = bytearray(RIP_HEADER_SIZE + num_rip_entries * 20)
  
  packet[0] = RESPONSE_PACKET_COMMAND_NUM
  packet[1] = RIP_VERSION_NUM
  
  #adding the own router ID
  packet[2] = own_router_id >> 8
  packet[3] = own_router_id - (own_router_id >> 8 << 8)
  
  for (i, router_id) in enumerate(router_id_keys):
    packet[4 + i*RIP_ENTRY_SIZE] = 0
    packet[5 + i*RIP_ENTRY_SIZE] = ADDRESS_FAMILY_IDENTIFIER
    packet[6 + i*RIP_ENTRY_SIZE] = packet[7 + i*RIP_ENTRY_SIZE] = 0 #these two bytes must be 0
    
    #split the destination address into bytes
    dest_addr = routing_table[router_id].destination_addr
    packet[8 + i*RIP_ENTRY_SIZE] = 0 #these are 0 because dest_addr cannot exceed 64000
    packet[9 + i*RIP_ENTRY_SIZE] = 0
    
    packet[10 + i*RIP_ENTRY_SIZE] = dest_addr >> 8
    dest_addr -= dest_addr >> 8 << 8
    packet[11 + i*RIP_ENTRY_SIZE] = dest_addr
    
    #these next fields are 0
    packet[12 + i*RIP_ENTRY_SIZE] = packet[13 + i*RIP_ENTRY_SIZE] = packet[14 + i*RIP_ENTRY_SIZE] = packet[15 + i*RIP_ENTRY_SIZE] = 0
    packet[16 + i*RIP_ENTRY_SIZE] = packet[17 + i*RIP_ENTRY_SIZE] = packet[18 + i*RIP_ENTRY_SIZE] = packet[19 + i*RIP_ENTRY_SIZE] = 0
    
    #adding metric
    #metric can only be 16 so these fields will always be 0
    packet[20 + i*RIP_ENTRY_SIZE] = packet[21 + i*RIP_ENTRY_SIZE] = packet[22 + i*RIP_ENTRY_SIZE] = 0
    packet[23 + i*RIP_ENTRY_SIZE] = routing_table[router_id].cost
    
  return packet






#routing_table = dict();

#route_1 = routing_table.Route(1234, 1234, 4321, 1, datetime.datetime.now())
#print(route_1)
#routing_table[1234] = route_1

#route_2 = Route(4321, 4321, 5321, 1, datetime.datetime.now())
#routing_table[4321] = route_2

#route_3 = Route(4021, 4021, 5121, 1, datetime.datetime.now())
#routing_table[4021] = route_3

#print(generate_rip_response_packet(1232, routing_table, [1234, 4321, 4021]))
    
  
  

    

