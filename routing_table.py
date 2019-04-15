"""
routing_table.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import datetime
import Link
import Route
from rip_packet import is_packet_valid, get_packet_data
    
    
  
def initialise_routing_table(routing_table, output_links):
  """
  Takes a list of directly connected output Links and initialises the given 
  routing table.
  """
  
  if len(routing_table) != 0 or type(routing_table) != dict:
    raise ValueError("The routing table must be an empty dictionary")
  
  for link in output_links:
    #put each directly connected route into the routing table
    routing_table[link.routerID] = Route.Route(link.routerID, link.routerID, link.port, link.metric, datetime.datetime.now())
 
    
    
def process_packet(routing_table, packet_bytearray):
  """
  Processes the packet according to the RIP specifiction. This function may or 
  may not edit the routing_table depending on the contents of the packet.
  """
  
  #only do anything if the packet is valid
  if is_packet_valid(packet_bytearray):
    
    sending_router_id, routes_list = get_packet_data(routing_table, packet_bytearray)
    
    
    for route in routes_list:
      existing_route = routing_table.get(route.destination_addr)
      
      #if no route exists in the current routing table and the cost is not infinite, then add to routing table
      if existing_route is None and route.cost < 16:
        route.time = datetime.datetime.now() #re-init time
        route.route_change_flag = True
        routing_table[route.destination_addr] = route
        
        
      #if we are already using this router to get to this location (i.e the router is updating us about a route we are using)
      elif existing_route.gateway == sending_router_id:
        routing_table[route.destination_addr].time = datetime.datetime.now() #re-init the timer
        
        #if the cost has changed
        if existing_route.cost != route.cost:
          routing_table[route.destination_addr].cost = route.cost #change the cost for the entry in the routing table
          routing_table[route.destination_addr].route_change_flag = True
          
          if (route.cost == 16):
            pass #start deletion process @@@
         
          
      #if we have just found a lower cost path, then add it to routing table    
      elif existing_route.cost > route.cost:
        route.time = datetime.datetime.now() #init the timer
        route.route_change_flag = True
        routing_table[route.destination_addr] = route #add to routing table
        
        
  else:
    print("*" * 10, "A packet has been dropped", "*" * 10)
          
          
          
        
        