"""
Route.py, Author: jbr185, 66360439, dwa110, 28749539
"""

import datetime

class Route(object):
  
  def __init__(self, address, first_hop_router_id, first_hop_port_num, cost, time, route_change=False):
    self.destination_addr = address
    self.gateway = first_hop_router_id
    self.gateway_port = first_hop_port_num
    self.cost = cost
    self.__start_time = time
    self.__end_time = time + datetime.timedelta(seconds=180)
    self.route_change_flag = route_change
    self.garbage_collection_time = None
    
  def __str__(self):
    return "Destination address: {}\nGateway: \n   Router ID: {}\n   Port Number: {}\nMetric: {}\nExpires: {}\nGarbage Collection Time: {}".format(self.destination_addr, self.gateway, self.gateway_port, self.cost, self.time, self.garbage_collection_time)
  
  @property
  def time(self):
    return self.__end_time
  
  @time.setter
  def time(self, time):
    self.__start_time = time
    self.__end_time = time + datetime.timedelta(seconds=180)