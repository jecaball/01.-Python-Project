#import required modules
from bokeh.plotting import figure, show
import numpy as np
import pandas as pd

#creates class
class Visualization():
    '''# Visualization\n

    ## Description:\n
    This class is to be used for the generation of scatter plots to show which values fall into the categories of the ideal function.\n\n

    ## Initilization arguments:\n
    None\n\n

    ## Parameters:\n
    source (pandas.DataFrame): Pandas dataframe containing the information to be plotted. The dataframe is made up of three columns named 'x', 'y', and 'ideal function
    which correspond to the pair (x,y) to be plotted and an indication to which ideal function the piar corresponds.\n
    xLabelName (str): String indicating the name to be used for the x-label.\n
    yLabelName (str): String indicating the name to be used for the y-label.\n
    plotTitle (str): String indicating the title to be used for the plot.
    '''
    # public properties of the class visualization
    source=pd.DataFrame() # source of the data required for plotting. It is a pandas dataframe with three columns-> x,y, and ideal function.
    xLabelName=str() # name to be used as x-label in the plot
    yLabelName=str() # name to be used as y-label in the plot
    plotTitle=str() # title to be used for the plot
    columnsCategories=str() #gets the name of the column with the categories
    legendTitle=str() #gets the legend title

    #defines the categories
    def __defineCategories(self)->None:

        #creates the column color category to store as indicated by the name
        self.source['Color Category']=''

        #gets the unique values for the color categories
        uniqueCategories=self.source[self.columnsCategories].unique()
        
        #define colors
        colors=['black','orange','blue','firebrick','green']

        #loops throught the different categories
        for cat, color in zip(uniqueCategories,colors):
            
            # fills up the column 'color category' of the pandas dataframe stored in source
            self.source.loc[self.source[self.columnsCategories]==cat,'Color Category']=color

        #returns results
        return None
    
    #creates plot with the x and y values and the labels given
    def createPlot(self)->None:
        '''# createPlot\n
        ## Description:\n
        Creates a plot based on the information given in source, xLabelName, yLabelName, and plotTitle.\n\n

        ## Arguments:\n
        None.\n

        ## Returns:\n
        None.\n
        '''

        #calls the function define categories for the definition of the cateogries and their color in the plot
        self.__defineCategories()

        #creates a function plot
        plot=figure(
            title=self.plotTitle,
            x_axis_label=self.xLabelName,
            y_axis_label=self.yLabelName,
            width=1000,
            height=1000,
            )

        # generates the scatter plot
        plot.scatter('x','y',legend_group=self.columnsCategories,color='Color Category',source=self.source,size=5)

        #adds a legend title
        plot.legend.title=self.legendTitle
        
        #shows the plot
        show(plot)

        #returns None
        return None
        