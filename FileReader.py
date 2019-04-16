"""
FileReader.py, Author: jbr185, 66360439, dwa110, 28749539

this file contains functions for reading config files
"""
from MyUtils import checkParameter
from Link import Link

def readConfig(filePath):
    try:
        routerID = -1 #the router id for out daemon
        inputPorts = [] #the input ports we are listening to
        outputLinks = [] #the output connections we are sending to
        otherRouterIDs = [] #for keeping track of the router IDs we have to ensure no duplicates

        #open the file for reading
        file = open(filePath, 'r')
        text = file.readlines()
        file.close()

        #for each line in the file
        for (index, line) in enumerate(text):
            line = line.strip() #remove any leading whitespace

            if len(line) == 0:
                continue #empty line
            elif line.startswith('#'): 
                continue #comment line
            elif line.startswith("router-id"):
                line = line.split(' ') #brake apart the two parts of this line, the second is our router id!

                routerID = checkParameter(line[1], int, 0, 64001) #bound between 1 and 64000 inclusive
                otherRouterIDs.append(routerID) #we don't want people using our ID withut some complaints
            elif line.startswith("input-ports"):
                line = line[line.find(' '):].split(',') #split after the "input-ports" sub string

                for interface in line: #check each port input
                    interface = checkParameter(interface, int, 1023, 64001) #bound between 1024 and 64000 inclusive
                                       
                    if not (interface in inputPorts) and not (interface in [output.port for output in outputLinks]): #ensure its unique
                        inputPorts.append(interface)
                    else:
                        raise ValueError("Inferface socket port already in use")
            elif line.startswith("outputs"):
                line = line[line.find(' '):].split(',') #split after "outputs"

                for output in line:
                    link = Link() #we need a containing link object
                    output = output.split('-') #split the parts of each output
                    output[0] = checkParameter(output[0], int, 1023, 64001)
                    
                    if not (output[0] in [output.port for output in outputLinks]) and not (output[0] in inputPorts):
                        link.port = output[0]
                    else:
                        raise ValueError("Inferface socket port already in use")
                        
                    link.metric = checkParameter(output[1], int, -1, 15) #second is the metric
                    output[2] = checkParameter(output[2], int, 0, 64001)
                    if not (output[2] in otherRouterIDs): #final is unique router id
                        otherRouterIDs.append(output[2])
                        link.routerID = output[2]
                    else:
                        raise ValueError("Router ID {} is duplicated in the configuration file. Router IDs must be unique.".format(output[2]))                    
            
                    outputLinks.append(link) #add the link port to the outputs
            else:
                raise SyntaxError("Syntax error in file \"{0}\", on line {1}".format(filePath, index + 1))
        return (routerID, inputPorts, outputLinks) #return the information in the file
    except (ValueError, TypeError) as error: #if we have some value or type error we have a syntax error in the file
        print(error)
        raise SyntaxError("Syntax error in file \"{0}\", on line {1}".format(filePath, index + 1))
