#import required modules
import numpy as np
import pandas as pd
import sqlalchemy as db

###creates databases to store information of stock prices and not having to download data all the time
class SQLCommunication():

    #properties
    __con=None    
    __engine=None
    __metadata=None
    __table=None
    fetchedData=None


    #constructor for parameters and modules to initate as soon as the object is created
    def __init__(self,database:pd.DataFrame,tablesName:str):
        #it will be taken as default parameters ticker ASML and interval of 15 minutes

        #stores the content of the variable database in the property database
        self.__database=database

        #defines the name of the database
        self.__tableName=tablesName

        #creates connection
        self.__createsConnection()
        
        #creates the table for the database of the ticker and the interval defined by user
        self.__createTable()

    #creates connection to database
    def __createsConnection(self)->None:
        """
        # Description:\n
        Creates a connection to the database. The database's location and name is already defined and cannot be modified.\n

        # Parameters:\n
        This is an internal module and requires no parameters.
        """
        
        # #path location of the database and file name
        # pathFile=os.path.dirname(__file__)
        #defines the name of the database
        databaseName='database'

        # #joins pathFile and fileName
        # fileLocation=os.path.join(pathFile,fileName)

        #try blocks to catch errors that might occur
        try:
            # gets engine object
            self.__engine=db.create_engine("mysql+pymysql://username:password@localhost/{}".format(databaseName))
           
            # gets engine object 
            self.__con=self.__engine.connect()

            #gets metadata object
            self.__metadata=db.MetaData()
            
        except Exception as e:
            print(e)

        #returns None
        return None
    
    #creates or opens tables
    def __createTable(self)->None:

        #try-block to catch errors
        try:

            #creates a table if this does not exists
            #adds the identification columns
            self.__table=db.Table(
                self.__tableName,
                self.__metadata,
                db.Column('id',db.Integer,primary_key=True,autoincrement=True,nullable=False),

            )

            #gets the columns names from the database
            columnsNames=self.__database.columns

            #loops through all the names and adds them as columns of the table
            for name in columnsNames:

                #adds the columns
                self.__table.columns.add(name,db.Float,primary_key=False,nullable=False)

                
        #potential exceptions here to be cathed
        except Exception as e:
            print(e)

        #returns None
        return None
        
    #adds new elements to a table
    def __insertNewValues(self)->None:
        
        #try block
        try:
            
            #prepares the insert statement
            sqlQuery=db.insert(self.__table)

            #prepares the list of the data
            dataList=self.__database.to_dict(orient='records')

            #executes the insert statement
            self.__con.execute(sqlQuery,dataList)

        except Exception as e:

            print('An error has ocurred: {}'.format(e))

        return None
    
    #downloads selected data 
    def __selectAndFetch(self)->None|pd.DataFrame:

        #try block to capture exceptions
        try:
           
           #makes the selection statement
           results=db.select([self.__table])

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
        
    def fetchAll(self)->pd.DataFrame:

        #returns all information available in the table
        return self.__selectAndFetch()
    
    