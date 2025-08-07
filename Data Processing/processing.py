import numpy as np
import pandas as pd

class Optimization():        

    #calculates the MSE between datasets
    def __leastSquares(self,dataset1:np.ndarray,dataset2:np.ndarray)->np.ndarray[float,float]:
        
        #gets the maximum deviation between points in the datasets
        maxDeviation=self.__maxDeviation(dataset1=dataset1,dataset2=dataset2)

        #returns the least squares
        return np.array([np.sum((dataset1-dataset2)**2),maxDeviation])
    
    #gets the maximum deviation from the dataset
    def __maxDeviation(self,dataset1:np.ndarray,dataset2:np.ndarray)->float:

        #calculates the difference between points in the datasets
        diff=dataset1-dataset2

        #calculates the absolute value
        diff=abs(diff)

        #returns the maximum difference
        return diff.max()

class Processing(Optimization):

    #additional properties
    comparisonResults=dict()    # stores the results of the comparion between train and ideal datasets
    candidateSelection=dict()   # stores the results of the selection of the best candidates

    def __init__(self, training:pd.DataFrame,test:pd.DataFrame,idealFunctions:pd.DataFrame):

        #defines properties
        self.__trainingDataset=training         # training data set as well identified as A in the document
        self.__testDataset=test                 # test data set as well identifies as B in the document
        self.__idealFunctions=idealFunctions    # ideal functions dataset as well identified as C in the document

    #converts data from pandas to numpy
    def __convertsPandasToNumpy(self,dataFrame:pd.DataFrame)->np.ndarray:

        #converts to numpy and resturn results
        return dataFrame.to_numpy()
    
    #compares training dataset against the ideal functions
    def __compareTrainingIdeal(self)->None:

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
                    self.__leastSquares(
                        dataset1=npTrainingDataset[:,dataset],
                        dataset2=npIdealFunctions[:,ideal]))
            
            #updates the variable comparison results
            self.comparisonResults.update(
                {'Dataset{}'.format(dataset):partialResults} #-----> check the structure of the results 
            )
        
        #returns results
        return None
    
    #selects the candidates from the ideal datasets
    def selectCandidates(self)->None:

        #loops through the datasets stored in comparison results
        for dataset in self.comparisonResults.keys():

            #gets the index of the min value of the least squares from every dataset
            self.candidateSelection.update({dataset:np.argmin(self.__compareTrainingIdeal[dataset])+1})

        #returns results
        return None
    
    #maps individual test cases (B) to the four ideal functions (A)
    def mappingTestCase(self)->np.ndarray:

        #converts the test dataset into a numpy array
        npTestDataset=self.__testDataset.to_numpy()
        
        #adds a column to npTestDataSet where will be indicated to which ideal function it belongs
        npTestDataset=np.c_[npTestDataset,np.zeros(shape=(len(npTestDataset)))]

        #converts the ideal functions data set into numpy array
        npIdealFunction=self.__idealFunctions.to_numpy()

        #gets the list of selected ideal function
        selectedCaditates=list(self.candidateSelection.values())

        #adds the column 0 to be able to compare at the same coordinates
        selectedCaditates.index(0,0)

        #filters the ideal function dataset such that only remains those which were selected
        npIdealFunction=npIdealFunction[:,selectedCaditates]

        #loops through all the points of npTestDataset
        for i









    





    



