#this python file is used for the creation of user-defined exceptions

class MissingPathFile(Exception):
    '''# MissingPathFile\n

    ## Description:\n
    This class is an user defined exception for when the path file is not provided. It is executed when the data type of the variable pathFile is None.\n\n

    ## Initilization arguments:\n
    pathFile (None|str): Location of the file as a string or None.\n
    msg (str): Error message.\n\n

    ## Parameters:\n
    None.
    '''

    def __init__(self, pathFile,msg='No pathfile was provided')->None:
        
        #defines properties to be initialized with thew object creation
        self.pathFile=pathFile
        self.msg=msg
        
        super().__init__(self.msg)

    #defines the string to be provided in case of an error
    def __str__(self)->str:

        #return results
        return f'{type(self.pathFile)} ->{self.msg}'