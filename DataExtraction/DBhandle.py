#import required modules
import numpy as np
import pandas as pd
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

###creates databases to store information
class SQLCommunication():
    '''
    # SQLCommunication\n
    ## Description:\n
    Handles the communication with the database management system based on sqlalchemy.\n\n

    ## Initilization arguments:\n
    database (pandas.DataFrame): Pandas dataframe contianing the data to be added to the database. The columns of the database are taken directly from the column names of the dataframe.\n
    tablesName (str):Name to be given to the table where the data is to be stored in the database mangement system.\n
    insertValues (bool): Indicates if the data is to be added inmidiatly to the table. \n\n
    
    ## Parameters:\n
    None.
    '''

    # private properties 
    __con=None      # variable to handle the contection to the engine
    __engine=None   # variable that handles the engine
    __metadata=None # variable to store the metadata of the object
    __table=None    # variable that stores the table object to handle the table

    #constructor for parameters and modules to initate as soon as the object is created
    def __init__(self,database:pd.DataFrame,tablesName:str,insertValues:bool=True)->None:

        #stores the content of the variable database in the property database
        self.__database=database

        #defines the name of the database
        self.__tableName=tablesName

        #creates connection
        self.__createsConnection()
        
        #creates the table for the database of the ticker and the interval defined by user
        self.__createTable()

        #if the variable insert values is true, then add the values of the variable database into the corresponding table
        if insertValues:

            self.insertNewValues()

        #if the variable insertValue is False, then do nothing
        else:

            #returns None
            return None

        #returns None        
        return None


    #creates connection to database
    def __createsConnection(self)->None:
        """
        # __createsConnection
        ## Description:\n
        Creates a connection to the database. The database's location and name is already defined and cannot be modified.\n

        ## arguments:\n
        This is an internal module and requires no parameters.
        """
        #defines the name of the database
        databaseName='database'

        #try blocks to catch errors that might occur
        try:
            # gets engine object
            self.__engine=db.create_engine("sqlite:///{}.db".format(databaseName))

            #checks if the database exists
            if not database_exists(self.__engine.url):

                #creates the database
                create_database(self.__engine.url)
           
            # gets engine object 
            self.__con=self.__engine.connect()

            #gets metadata object
            self.__metadata=db.MetaData()
            
        except Exception as e:#---->correct this exception name to add the adequate one

            print(e)

        #returns None
        return None
    
    #creates or opens tables
    def __createTable(self)->None:
        """
        # __createTable\n\n
        # Description:\n
        Creates a table in the database with the information obtained from the dataframe.\n

        # arguments:\n
        This is an internal module and requires no parameters.
        """

        #try-block to catch errors
        try:

            #creates a table if this does not exists
            #adds the identification columns
            self.__table=db.Table(
                self.__tableName,
                self.__metadata,
                db.Column('id',db.Integer,primary_key=True,autoincrement=True,nullable=False)
            )
            
            #gets the columns names from the database
            columnsNames=self.__database.columns

            #loops through all the names and adds them as columns of the table
            for name in columnsNames:

                #adds the columns
                self.__table.append_column(db.Column(name,db.Float,primary_key=False))

            #creates the table with the indicated columns
            self.__metadata.create_all(self.__engine)

        #potential exceptions here to be cought
        except Exception as e:
            print(e)

        #returns None
        return None
        
    #adds new elements to a table, this new elements come from the previously given pandas DataFrame
    def insertNewValues(self,dataset:pd.DataFrame|None=None)->None:
        """
        # insertNewValues\n\n
        # Description:\n
        Inserts new values to the table in the database management system.\n

        # arguments:\n
        dataset (pandas.DataFrame | None): if dataset is a pandas dataframe, then the information in the pandas dataframe will be inserted in the table. Otherwise, 
        it will be inserted the information given at the initilization of the object.\n

        # Returns:\n
        None.
        """
        
        #try block to catch for errors
        try:
            
            #prepares the insert statement
            sqlQuery=db.insert(self.__table)

            if dataset is None:

                #prepares the list of the data
                dataList=self.__database.to_dict(orient='records')

            elif type(dataset)==pd.DataFrame:

                dataList=dataset.to_dict(orient='records')

            #executes the insert statement one by one to check add new rows only when they bring new information
            for data in dataList:

                #make a select statement for a table
                selectStatemten=db.select(self.__table).where(self.__table.c.x==data['x'])

                #excutes the statement
                fetchedResults=self.__con.execute(selectStatemten).fetchall()

                #if the data is already there, do nothing
                if len(fetchedResults)!=0 and data['x'] == fetchedResults[0][1]:
                    
                    continue
                
                #else, adds the information into the database
                else:
                
                    self.__con.execute(sqlQuery,data)

            #commits to the insertion of the data
            self.__con.commit()

        except Exception as e:

            print('An error has ocurred: {}'.format(e))

        return None
      
    #downloads selected data 
    def __selectAndFetch(self)->None|pd.DataFrame:

        """
        # __selectAndFetch\n\n
        # Description:\n
        Fetches all the information available in the table of the database management system.\n

        # arguments:\n
        This is an internal module and requires no parameters.

        # Returns:\n
        None when an error happened or a pandas DataFrame with the requested information.
        """

        #try block to capture exceptions
        try:
           
           #makes the selection statement
           results=self.__table.select()

           #executes the selection statement
           results=self.__con.execute(results).fetchall()

           #converst to dataframe
           results=pd.DataFrame(data=results)

           #return results
           return results

        except Exception as e:
            print('An error has ocurred. {}'.format(e))

            #returns None
            return None
    
    #fetches all the information available in the table
    def fetchAll(self)->pd.DataFrame:
        """
        # fetchAll\n\n
        # Description:\n
        Fetches all the information available in the table of the database mangement system.\n

        # arguments:\n
        None.\n

        # Returns:\n
        pd.DataFrame with the information available in the table.
        """

        #returns all information available in the table
        return self.__selectAndFetch()
    