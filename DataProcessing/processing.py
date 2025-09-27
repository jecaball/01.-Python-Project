import numpy as np
import pandas as pd

class Optimization():
    '''# Optimization\n

    ## Description:\n
    Contains modules for calculation of the error between two datasets.\n\n

    ## Parameters:\n
    None.
    '''      

    #calculates the MSE between datasets and gets the maximum deviation between the datasets
    def leastSquares(self,dataset1:np.ndarray,dataset2:np.ndarray)->np.ndarray[float,float]:
        """
        # leastSquares\n\n
        ## Description:\n
        Calculates the least squares between dataset1 and dataset2 arrays.\n

        ## arguments:\n
        dataset1 (numpy.ndarray): Numpy array with pair x,y.\n
        dataset2 (numpy.ndarray): Numpy array with pair x,y.\n

        ## Returns:\n
        Numpy array with least squarea and maximum deviation between datasets.
        """

        #gets the maximum deviation between points in the datasets
        maxDeviation=self.__maxDeviation(dataset1=dataset1,dataset2=dataset2)

        #returns the least squares
        return np.array([np.sum((dataset1-dataset2)**2),maxDeviation])
    
    #gets the maximum deviation from the dataset
    def __maxDeviation(self,dataset1:np.ndarray,dataset2:np.ndarray)->float:
        """
        # __maxDeviation\n\n
        ## Description:\n
        Gets the maximum deviation from between points of the datasets.\n

        ## arguments:\n
        dataset1 (numpy.ndarray): Numpy array with pair x,y.\n
        dataset2 (numpy.ndarray): Numpy array with pair x,y.\n

        ## Returns:\n
        float that corresponds to the maximum difference.
        """

        #calculates the difference between points in the datasets
        diff=dataset1-dataset2

        #calculates the absolute value
        diff=abs(diff)

        #returns the maximum difference
        return diff.max()

class Processing(Optimization):
    '''
    # Processing\n
    ## Description:\n
    Compares training and ideal data to select the candidates that will be mapped in the test case database.\n\n

    ## Initilization arguments:\n
    training (pandas.DataFrame): Pandas dataframe contianing the data training dataset.\n
    test (pandas.DataFrame): Pandas dataframe contianing the test training dataset.\n
    idealFunctions (pandas.DataFrame): Pandas dataframe contianing the ideal functions dataset. \n\n
    
    ## Properties:\n
    comparisonResults (dict): Stores the results of the comparion between train and ideal datasets\n
    candidateSelection (dict): stores the results of the selection of the best candidates\n
    '''

    #additional properties
    comparisonResults=dict()    # stores the results of the comparion between train and ideal datasets
    candidateSelection=dict()   # stores the results of the selection of the best candidates

    def __init__(self, training:pd.DataFrame,test:pd.DataFrame,idealFunctions:pd.DataFrame):

        #defines properties
        self.__trainingDataset=training         # training data set as well identified as A in the document
        self.__testDataset=test                 # test data set as well identifies as B in the document
        self.__idealFunctions=idealFunctions    # ideal functions dataset as well identified as C in the document

        #makes the comparison between training and ideal functions dataset
        self.__compareTrainingIdeal()

    #converts data from pandas to numpy
    def __convertsPandasToNumpy(self,dataFrame:pd.DataFrame)->np.ndarray:
        """
        # __convertsPandasToNumpy\n\n
        ## Description:\n
        converts data from pandas to numpy.\n

        ## arguments:\n
        dataFrame (pandas.DataFrame): Pandas dataframe to be converted to numpy.ndarray.\n

        ## Returns:\n
        Numpy.ndarray.
        """

        #converts to numpy and resturn results
        return dataFrame.to_numpy()
    
    #compares training dataset against the ideal functions
    def __compareTrainingIdeal(self)->None:
        """
        # __compareTrainingIdeal\n\n
        ## Description:\n
        Compares training dataset against the ideal functions.\n

        ## arguments:\n
        None.\n

        ## Returns:\n
        None.
        """

        #gets numpy version of the training dataset
        npTrainingDataset=self.__convertsPandasToNumpy(self.__trainingDataset)

        #gets the numpy version of the ideal funtion dataset
        npIdealFunctions=self.__convertsPandasToNumpy(self.__idealFunctions)

        #loops through training datasets
        for dataset in range(1,len(npTrainingDataset[0,:])):
            
            #stores partial results form least squares function calculation
            partialResults=np.array([])

            #loops through the ideal functions datasets
            for ideal in range(1,len(npIdealFunctions[0,:])):
                
                #calculates the least squares and appends the results into the variable partial results
                partialResults=np.append(
                    partialResults,
                    self.leastSquares(
                        dataset1=npTrainingDataset[:,dataset],
                        dataset2=npIdealFunctions[:,ideal]))
            
            #rashapes the results such that column 0 contains the loss function and column 1 contains the maximum deviation
            partialResults=partialResults.reshape((int(len(partialResults)/2),2))

            #updates the variable comparison results
            self.comparisonResults.update(
                {'Dataset{}'.format(dataset):partialResults} 
            )
        
        #returns results
        return None
    
    #selects the candidates from the ideal datasets
    def selectCandidates(self)->None:
        """
        # selectCandidates\n\n
        ## Description:\n
        Selects the candidates from the ideal datasets.\n

        ## arguments:\n
        None.\n

        ## Returns:\n
        None.
        """

        #loops through the datasets stored in comparison results
        for dataset in self.comparisonResults.keys():

            #gets the index of the min value of the least squares from every dataset
            self.candidateSelection.update({dataset:int(np.argmin(self.comparisonResults[dataset][:,0])+1)})

        #returns results
        return None
    
    #maps individual test cases (B) to the four ideal functions (A)
    def mappingTestCase(self)->np.ndarray:
        """
        # mappingTestCase\n\n
        ## Description:\n
        Maps individual test cases (B) to the four ideal functions (A).\n

        ## arguments:\n
        None.\n

        ## Returns:\n
        Numpy.ndarray.
        """

        #converts the test dataset into a numpy array
        npTestDataset=self.__testDataset.to_numpy()

        #converts the ideal functions data set into numpy array
        npIdealFunction=self.__idealFunctions.to_numpy()

        #gets the list of selected ideal function
        selectedCaditates=list(self.candidateSelection.values())

        #adds the column 0 to be able to compare at the same coordinates
        selectedCaditates.insert(0,0)

        #filters the ideal function dataset such that only remains those which were selected
        npIdealFunction=npIdealFunction[:,selectedCaditates]

        #loops through all the points of npTestDataset
        for i in range(0, len(npTestDataset)):
            
            #gets the x value 
            xValue=npTestDataset[i,0]
            
            #gets the index of the xValue from the npIdealFunction array
            index=int(np.where(npIdealFunction[:,0]==xValue)[0])
            
            #loops through all the idea functions
            for j in range(0,4):
                                
                if abs(float(npTestDataset[i,1])-float(npIdealFunction[index,j+1]))<=abs(np.sqrt(2)*self.comparisonResults['Dataset{}'.format(j+1)][selectedCaditates[j+1]-1,1]): ###### to be corrected ---> it needs to be very well defined where the maximum difference is coming from

                    #adds the index of the column if the conditions are True
                    npTestDataset[i,2]=int(selectedCaditates[j+1])

                    #if found early, break the loop
                    break

            

        #returns the results 0 means there is no coincidence, other number means the column with the ideal function
        return npTestDataset