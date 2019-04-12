"""
MyUtils.py, author: jbr185, 66360439

Just some helpful functions for my python coding
"""
from sys import argv, exit
from math import inf

def getCommandLineArgument(index, dataType, lowerBound=-inf, upperBound=inf, correction=False):
    """
    This function gets the commandline argument of the given index in the given datatype. if the value 
    cannot be converted a TypeError is thrown. if the value is a number it can be bounded, if the arg
    is outside this range a ValueError is thrown. if correction is set to true the user will be prompted
    to correct the argument.
    """
    try:
        value = dataType(argv[index + 1]) #try to convert the argument to the given dataType
        while dataType in [int, float] and (value < lowerBound or value > upperBound):
            #if the value is outside the given range (if bounded is true) report
            print("Argument", index, "is invaild, Please type a number between", lowerBound, "and", upperBound)
            if not correction: #if correction is False exit the program
                pause()
                exit(-1)            
            try:
                return dataType(input("> ")) #try to convert the corrected value
            except ValueError:
                continue
        return value
    except ValueError: #if value is not of type given
        raise TypeError("argument cannot be converted to given type")   
    
def getInput(prompt="", dataType=str, lowerBound=-inf, upperBound=inf):
    """
    Prompts the user for an input, a prompt can be given along with a dataType to convert to. if the value
    cannot be converted to the given type then the user will be prompted to input a new value. If the data
    type is a number (float or int) then the value can be bounded to a given upper and lower limit
    """
    print(prompt)
    result = input("> ")
    while True:
        try:
            result = dataType(result) #try to convert to data type given
            if (dataType in [int, float] and (result < lowerBound or result > upperBound)):
                #if the value in not in the given range (and bounded is True) prompt the user to try again
                print("Please type a number between", lowerBound, "and", upperBound)
                result = input("> ")
            else:
                return result
        except ValueError: #if the input cannot be converted to the datatype, prompt the user to retry
            print("Invalid Input!")
            result = input("> ")

def checkParameter(parameter, dataType, lowerBound=-inf, upperBound=inf):
    """
    Checks the given parameter if it is the given data type, if the type is in float or int then the value
    can be bounded within a range. throws a TypeError if the paramter cannont be converted to the given 
    datatypr. throws a ValueError if the value is not in the given range. returns the converted value
    """
    try:
        parameter = dataType(parameter) #attempt to convert to the dataType
        if (dataType in [int, float] and parameter > lowerBound and parameter < upperBound):
            #if the value is a number check its bounds
            return parameter #return converted value
        else:
            raise ValueError("Given value is not in the given range")
    except ValueError: #cannot convert, throw a TypeError
        raise TypeError("Given value cannot be converted to the given data type")
    


def pause(prompt="Press Enter to Continue..."):
    """
    Pauses the console until the user presses the Enter key. A custom prompt can be given
    """
    input(prompt)