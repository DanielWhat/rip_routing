"""
Link.py, author: jbr185, 66360439

This is the class for a router link in particular daemon
"""

class Link:
    """
    This class simply holds the data for a link so it can be indexed more readably
    """
    def __init__(self):
        self.port = -1 #the port this link is on
        self.metric = -1 #the cost of the link
        self.routerID = -1 #the ID of the router on the otherside

    def __str__(self):
        return "(Link: port = {0}, metric = {1}, routerID = {2})".format(self.port, self.metric, self.routerID)
