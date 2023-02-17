## function to check type of input
## takes a type and a value and throws an error if the type is not correct
def check_type(type, value):
    if type(value) != type:
        raise TypeError("Expected type " + str(type) + " but got " + str(type(value))) 
    else:
        return True