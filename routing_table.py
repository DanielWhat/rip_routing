"""
routing_table.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import datetime
import Link

class Route(object):
  
  def __init__(self, address, first_hop_router_id, first_hop_port_num, cost, time):
    self.destination_addr = address
    self.gateway = first_hop_router_id
    self.gateway_port = first_hop_port_num
    self.cost = cost
    self.__start_time = time
    self.__end_time = time + datetime.timedelta(seconds=90)
    
  def __str__(self):
    return "Destination address: {}\nGateway: \n   Router ID: {}\n   Port Number: {}\nMetric: {}\nExpires: {}".format(self.destination_addr, self.gateway, self.gateway_port, self.cost, self.time)
  
  @property
  def time(self):
    return self.__end_time
  
  @time.setter
  def time(self, time):
    self.__start_time = time
    self.__end_time = time + datetime.timedelta(seconds=90)
    
    
  
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
    
  