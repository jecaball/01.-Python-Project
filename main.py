#####import required modules#####
import numpy as np
import pandas as pd
import sqlalchemy as db
from DataProcessing.processing import Optimization


#Data Extraction
from DataExtraction.Readcsv import HandleCSV            # handles the csv files 
from DataExtraction.DBhandle import SQLCommunication    # handles communication with the DBMS

# Data processing
from DataProcessing.processing import Processing        # processes the data

# Data vizualisation
from DataPresentation.Visualization import Visualization# draws the data

# creates the function main which will be used for the execution of the program
def main()->None:

    #gets the databases
    #gets the dataset for training
    trainDataset=HandleCSV(filePath=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\train.csv'
                           ).getDataAsDataFrame()
    #gets the ideal functions dataset
    idealFunctionsDataset=HandleCSV(filePath=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\ideal.csv'
                                    ).getDataAsDataFrame()
    #gets the dataset for testing
    testDataset=HandleCSV(filePath=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\test.csv'
                          ).getDataAsDataFrame()
    
    # adds an additional column to the test dataset.
    #this column will store to which ideal function can be assigned to. 0-> no assigned, any other number corresponds to the position of the 
    # ideal function
    testDataset['ideal Function']=0
    
    #stores the databases into DBMS
    #stores the train dataset into train table
    train=SQLCommunication(database=trainDataset,tablesName='Table 1')
    #stores the ideal function database into the ideal table
    ideal=SQLCommunication(database=idealFunctionsDataset,tablesName='Table 2')
    #stores the test dataset into the test table
    test=SQLCommunication(database=testDataset,tablesName='Table 3',insertValues=False)

    #processes the data, selects the four ideal functions according to the train dataset
    processing=Processing(training=trainDataset,test=testDataset,idealFunctions=idealFunctionsDataset)
    
    #selects the candidates of the ideal function
    processing.selectCandidates()

    #maps the test case to every ideal function
    npTestDataset=processing.mappingTestCase()

    #fills up the testdataset varaible with the assigned ideal functions
    testDataset['ideal Function']=npTestDataset[:,2]
  
    #fills up Table 3 with the information contained in testdataset
    test.insertNewValues(dataset=testDataset)

    #creates a visualization objects for test dataset, training data, and the chosen ideal functions
    visTestDataset=Visualization()
    visTrainingData=Visualization()
    visIdealFunctions=Visualization()

    #####
    #adds all the properties necessary for the visualization of the test data set
    visTestDataset.source=testDataset
    visTestDataset.xLabelName='X-values [N.A.]'
    visTestDataset.yLabelName='Y-values [N.A.]'
    visTestDataset.plotTitle='Assignment of Ideal Functions'
    visTestDataset.columnsCategories='ideal Function'
    visTestDataset.legendTitle='Ideal Functions'
        
    #plots the results
    visTestDataset.createPlot()

    #####
    #prepares variable for usage 
    meltedTrainDataset=trainDataset.melt(id_vars=['x'])

    #corrects the name of a column variable
    meltedTrainDataset.rename(columns={'value':'y'},inplace=True)

    #adds all the properties necessary for the visualization of the training dataset
    visTrainingData.source=meltedTrainDataset
    visTrainingData.xLabelName='X-values [N.A.]'
    visTrainingData.yLabelName='Y-values [N.A.]'
    visTrainingData.plotTitle='Training Dataset'
    visTrainingData.columnsCategories='variable'
    visTestDataset.legendTitle='Training Dataset'

    #plots the results
    visTrainingData.createPlot()

    #####
    #prepares vairiable for plotting
    meltedIdealFunctionsDataset=idealFunctionsDataset.iloc[:,np.unique(npTestDataset[:,2]).astype(int).tolist()].melt(id_vars=['x'])
    
    #corrects the name of a column variable
    meltedIdealFunctionsDataset.rename(columns={'value':'y'},inplace=True)

    #adds all the properties necessary for the visualization of the training dataset
    visIdealFunctions.source=meltedIdealFunctionsDataset
    visIdealFunctions.xLabelName='X-values [N.A.]'
    visIdealFunctions.yLabelName='Y-values [N.A.]'
    visIdealFunctions.plotTitle='Chosen Ideal Functions'
    visIdealFunctions.columnsCategories='variable'
    visIdealFunctions.legendTitle='Chosen Ideal Functions'

    #plots the results
    visIdealFunctions.createPlot()

    #returns None
    return None


#import unittest for the testing of the code
import unittest

#creates the class UnitTestHandleCSV for the testing of the class
class UnitTestHandleCSV(unittest.TestCase):

    #required file path location for the execution of the modules
    filePath=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\train.csv'

    def test__loadFileDataFrame(self)->None:

        '''
        Tests the function __loadFileDataFrame.
        '''

        checkParameter=HandleCSV(filePath=self.filePath)

        #checks if the result is as expected-> pd.DataFrame
        self.assertIsInstance(checkParameter._HandleCSV__dataframe,pd.DataFrame,msg='The file should be an instace of pandas.DataFrame')

    def testgetDataAsDataFrame(self)->None:

        '''
        Tests the function getDataAsDataFrame.
        '''

        checkParameter=HandleCSV(filePath=self.filePath)

        #checks if the result is as expected-> pd.DataFrame
        self.assertIsInstance(checkParameter.getDataAsDataFrame(),pd.DataFrame,msg='The file should be an instace of pandas.DataFrame')

#creates the class UnitTestHandleCSV for the testing of the class
class UnitTestSQLCommunication(unittest.TestCase):
    
    #required to test communication with the database
    testDatabase=pd.DataFrame(data={'x':[1,2,3,4,5],'y':[6,7,8,9,10]})

    def test__createsConnection(self)->None:

        '''
        Tests the function __createsConnection.
        '''

        checkParameter=SQLCommunication(database=self.testDatabase,
            tablesName='TestTable',
            insertValues=False)

        #checks if the result is as expected-> MetaData
        self.assertIsInstance(checkParameter._SQLCommunication__metadata,db.MetaData,msg='The file should be an instace of sqlalchemy.MetaData')

    def test__createTable(self)->None:

        '''
        Tests the function __createTable.
        '''

        checkParameter=SQLCommunication(database=self.testDatabase,
            tablesName='TestTable',
            insertValues=False)

        #checks if the result is as expected-> Table
        self.assertIsInstance(checkParameter._SQLCommunication__table,db.Table,msg='The file should be an instace of sqlalchemy.Table')

    def testInsertNewValues(self)->None:

        '''Test the function InsertNewValues'''

        checkParameter=SQLCommunication(database=self.testDatabase,
            tablesName='TestTable',
            insertValues=False)
        
        #inserts the values into the table
        checkParameter.insertNewValues(dataset=self.testDatabase)

        #fetches the results from the table
        results=checkParameter.fetchAll()

        #checks if the result is as expected-> Table
        self.assertIsInstance(results,pd.DataFrame,msg='The file should be an instace of pandas.DataFrame')

#creates class for testing of the class optimization
class UnitTestOptimization(unittest.TestCase):
    
    #required data for the test
    dataset1=np.array([1,2,3,4,5,6,7,8,9,10])
    dataset2=np.array([1,2,3,4,5,6,7,8,9,10])

    def testLeastSquares(self)->None:

        '''
        Tests the function leastSquare.
        '''
    
        #starts a new object
        checkParameter=Optimization()

        #calls the module least square
        results=checkParameter.leastSquares(dataset1=self.dataset1,dataset2=self.dataset2)

        #checks if the result is as expected-> the length of the results shall be 2
        self.assertEqual(len(results),2,msg='The length of the file shall be 2')

    def testLeastSquares2(self)->None:

        '''
        Tests the function leastSquare.
        '''
    
        #starts a new object
        checkParameter=Optimization()

        #calls the module least square
        results=checkParameter.leastSquares(dataset1=self.dataset1,dataset2=self.dataset2)

        #checks if the result is as expected-> the difference shall be 0
        self.assertEqual(results[0],0,msg='The difference shall be 0')


#creates class for testing of the class processing
class UnitTestprocessing(unittest.TestCase):
    
    #required data for the test
    training=pd.read_csv(
        filepath_or_buffer=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\train.csv')
    test=pd.read_csv(
        filepath_or_buffer=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\test.csv'
    )
    idealFunctions=pd.read_csv(
        filepath_or_buffer=r'C:\Users\jorge\OneDrive\17. MSc Artificial Intelligence\01. First Semester\01. Programming with Python\01. Python Project\ideal.csv'
    )

    def testSelectCandidates(self)->None:

        '''
        Tests the function selectCandidates.
        '''

        self.test['ideal Function']=0

        #starts a new object
        checkParameter=Processing(training=self.training,test=self.test,idealFunctions=self.idealFunctions)

        #calls the module selectCandidates
        checkParameter.selectCandidates()

        #checks if the result is as expected-> the candidate selection variable shall be a dictionary
        self.assertIsInstance(checkParameter.candidateSelection,dict,msg='The parameter candidateSelection shall be an instance of dict')

main()

unittest.main()
#change to comply with 1.3 Additional task
    
   


