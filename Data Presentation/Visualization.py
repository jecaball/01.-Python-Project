#import required modules
from bokeh.plotting import figure,show
import numpy as np

#creates class
class Visualization():

    #properties
    xLabelName=str()
    yLabelName=str()
    plotTitle=str()
    xValues=np.array()
    yValues=np.array()

    #creates plot with the x and y values and the labels given
    def createPlot(self)->None:

        #creates a function plot
        plot=figure(title=self.plotTitle,x_axis_label=self.xLabelName,y_axis_label=self.yLabelName)

        
        #adds data for the generation of the scatter points
        plot.scatter(x=self.xValues,y=self.yValues)

        #returns results None
        return None
        