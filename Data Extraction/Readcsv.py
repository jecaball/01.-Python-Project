#imports modules
import pandas as pd
import tkinter as tk
from tkinter import filedialog


#creates a class that handles the search and download of the database from the .cvs-files
class HandleCSV():
    '''# HandleCSV\n
    ## Description:\n
    Handles *.csv files and provides a DataFrame type variable with the information contained in the file.\n\n

    ## Arguments:\n
    filePath (str|None): string with file path to the location of the file which. If None is provided then a pop-up window will be provided select the file.
    '''

    #spaces for properties
    #No additional properties

    #initialization module
    def __init__(self,filePath:str|None=None)->None:

        #initializes parameters
        self.__filePath=filePath

        #executes modules
        self.__checkParametersDataType()

        #loads the file into an internal parameter
        self.__loadFileDataFrame()
        
        #returns None
        return None
    
    #checks the datatype of the parameters __filneName and __pathFile
    def __checkParametersDataType(self)->None: 
        '''# __checkParametersDataType\n
        ## Description:\n
        Checks the data type of the parameters which are used to initialize the HandleCSV-object. 
        Compels the user to select a file with the help of a dialog window until a file of the correct format is selected.\n\n

        ## Arguments:\n
        None.\n

        ## Return:\n
        None.\n
        '''
        
        #try block to catch errors
        try:

            #checks if the variables fileName and pathfile are empty or not
            if self.__filePath is None:

                #indicates that one of the properties is None. Thus, the user will have to look after the files with a window
                print('The parameter is a None-type. Please, select the file you want to read with the following window.')

                #opens up a window to search for the file
                while True:
                    root=tk.Tk(screenName='Select file')
                    root.withdraw()

                    #gets the filepath
                    self.__filePath=filedialog.askopenfilename(defaultextension='csv')
                    
                    #checks if something was selected
                    if self.__filePath.endswith('.csv'):

                        #gets out of the loop
                        break

                    #otherwise, indicates you that you need to pick up a file
                    else:

                        print('No file was selected. Please select one.')
                        continue
            
            #if the data type is string, then check at least that the extension is correct
            elif type(self.__filePath)==str:

                if self.__filePath.endswith('.csv'):
                    pass #do nothing
                
                #informs that the data type is incorrect and ask to select a file with a dialog window
                else:

                    print('The file has the wrong data type. Please, select a file with the following dialog window')

                    #makes the parameter filePath None and executes this function again
                    self.__filePath=None

                    self.__checkParametersDataType()

            else:

                #informs that the wrong type of paramerter was used
                print('An error has occured. The parameter filePath is {} type.\n'\
                'Please, select a file with the following dialog window.'.format(type(self.__filePath)))
                return None
        
        #catch exceptions
        except Exception as e:

            print('An unexpected error has ocurred: {}'.format(e))

        #after everything was done, just return None
        finally:

            #returns None
            return None
        
    #loads into a dataframe-type variable
    def __loadFileDataFrame(self)->None:
        '''# __loadFileDataFrame\n
        ## Description:\n
        Loads the selected *.csv file into a pandas dataframe.\n\n

        ## Arguments:\n
        None.\n

        ## Return:\n
        None.\n
        '''
        #try block to catch for errors
        try:
            self.__dataframe=pd.read_csv(
                filepath_or_buffer=self.__filePath,
                header=1

            )

        except Exception as e:

            #informs that an error was detected
            print('An error has ocurred: {}'.format(e))

        finally:
            
            #returns None
            return None        
        
    #gets the file
    def getDataAsDataFrame(self)->pd.DataFrame:
        '''# getDataAsDataFrame\n
        ## Description:\n
        Returns a deep copy of the dataframe associated with the .csv file selected.\n\n

        ## Arguments:\n
        None.\n

        ## Return:\n
        Pandas.DataFrame.\n
        '''
        #returns a copy of the dataframe
        return self.__dataframe.copy(deep=True)
