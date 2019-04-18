"""
routing_table.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import datetime
import Link
from Route import Route
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
    routing_table[link.routerID] = Route(link.routerID, link.routerID, link.port, link.metric, datetime.datetime.now())
 
    
    
def process_packet(router, packet_bytearray):
  """
  Processes the packet according to the RIP specifiction. This function may or 
  may not edit the routing_table depending on the contents of the packet.
  """
  
  #only do anything if the packet is valid
  if is_packet_valid(packet_bytearray, router):
    sending_router_id, routes_list = get_packet_data(router, packet_bytearray)
    
    link_to_sending_router = [link for link in router.output_links if link.routerID == sending_router_id][0]
    sending_router_gateway_port = link_to_sending_router.port
    cost_to_sending_router = link_to_sending_router.metric     
    
    #since sending_router_id is a directly connected router the first condition can only be true if; a directly connected router went down, 
    #became unreachable, was deleted from the routing table, and is now back up.
    #
    #the second condition is for when a router comes out of garbage collection, and we were previously using an indirect route to get to them (see test_2)
    if router.routing_table.get(sending_router_id) == None or router.routing_table[sending_router_id].cost > cost_to_sending_router: 
      #make a new route for the deleted directly connected router
      direct_route = Route(sending_router_id, sending_router_id, sending_router_gateway_port, cost_to_sending_router, datetime.datetime.now())
      
      #add this directly connected router back into the routing table
      router.routing_table[sending_router_id] = direct_route  
      
      
    #if the current optimal route to the sending router is going directly to the sending router
    elif router.routing_table[sending_router_id].gateway == sending_router_id:
      router.routing_table[sending_router_id].cost = cost_to_sending_router #re-initialise the cost (this covers an edge case where the route goes into garbage collection)
      router.routing_table[sending_router_id].time = datetime.datetime.now() #we just received an update from this router so the link we are using must be working => refresh
      router.routing_table[sending_router_id].garbage_collection_time = None #if we were garbage collecting before, we shouldn't be anymore    
    
    
    for route in routes_list:
      existing_route = router.routing_table.get(route.destination_addr)
      
      #if no route exists in the current routing table and the cost is not infinite, then add to routing table
      if existing_route is None and route.cost < 16:
        #make sure it's not a route to ourselves!
        if (route.destination_addr != router.router_id):
          route.time = datetime.datetime.now() #re-init time
          router.routing_table[route.destination_addr] = route
          
        
      elif existing_route is None and route.cost >= 16: #no point in adding a new route that is un-usable
        pass
        
        
      #if we are already using this router to get to this location (i.e the router is updating us about a route we are using)
      elif existing_route.gateway == sending_router_id:
        router.routing_table[route.destination_addr].time = datetime.datetime.now() #re-init the timer
        
        #if the cost has changed
        if existing_route.cost != route.cost:
          router.routing_table[route.destination_addr].cost = route.cost #change the cost for the entry in the routing table
          router.routing_table[route.destination_addr].garbage_collection_time = None #if we were garbage collecting before, we shouldn't be anymore
          
          if (route.cost == 16):
            #the route should be garbage collected 120 seconds from now
            router.routing_table[route.destination_addr].garbage_collection_time = datetime.datetime.now() + datetime.timedelta(seconds=120)
            router.routing_table[route.destination_addr].route_change_flag = True #Andreas said to only to implement triggered updates for invalid routes.
         
          
      #if we have just found a lower cost path, then add it to routing table    
      elif existing_route.cost > route.cost:
        route.time = datetime.datetime.now() #init the timer
        router.routing_table[route.destination_addr] = route #add to routing table
        
  else:
    print("*" * 10, "An invalid packet has been dropped", "*" * 10)
          
          
          
        
        