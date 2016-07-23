# TODO:

from RelativeDrawing import *

class Graph(object):
    '''
    Stores the data about a parameter and slowly draws a graph in real time.
    '''
    
    def __init__(self, name, parameterList, colourList, minY, maxY, incrementX = 0.001, relX=0.55, relY=0.05, relWidth=0.4, relHeight=0.25, boxX = 0.5, boxY = 0.03, boxWidth = 0.5, boxHeight = 0.32, boxColour = color(255, 0, 0), axesColour = color(0)):
        '''
        Sets up a graph and draws on the axes.
        relX, relY, relWidth and relHeight determine the size of the actual graph and axes
        boxX, boxY, boxWidth, boxHeight determine the size of the containing box
        scalingY is the amount by which the y coordinate is scaled, and incrementX is the amount to increase X (time) for each plot
        parameterList contains the parameters to plot, and colourList is the colours to plot them in     
        '''
        self.name = name
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        self.boxX = boxX
        self.boxY = boxY
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.minY = minY
        self.maxY = maxY
        self.scalingY = relHeight / float(maxY - minY)
        self.incrementX = incrementX
        self.parameterList = parameterList
        self.colourList = colourList
        self.boxColour = boxColour
        self.axesColour = axesColour
    
    def display(self):
        '''
        Resets the graph and sets up the axes when required.
        More code may be added later to deal with drawing scales properly.
        '''
        # Draw the surrounding rectangle, getting rid of everything from before.
        noStroke()
        fill(self.boxColour)
        relXRect(self.boxX, self.boxY, self.boxWidth, self.boxHeight)
        
        # Draw the two axes
        stroke(self.axesColour)
        strokeWeight(2)
        
        # Decide on where the x axis should be.
        
        if self.minY <= 0 <= self.maxY:
            pointY = self.scalingY * self.minY + self.relY + self.relHeight
        elif self.minY > 0:
            pointY = self.relY + self.relHeight
        else:
            pointY = self.relY
        
        relXLine(self.relX, pointY, self.relX + self.relWidth, pointY) # x axis
        relXLine(self.relX, self.relY, self.relX, self.relY + self.relHeight) # y axis
        
        strokeWeight(1)
        
        # Draw in key
        drawingX = self.boxX + 0.05 * self.boxWidth
        keyWidth = 0.9 * self.boxWidth / len(self.parameterList)
        for i in range(len(self.parameterList)):
            # Draw a block of that colour
            fill(self.colourList[i])
            relXRect(drawingX, self.relY + 1.02 * self.relHeight, 0.05 * self.relWidth, 0.05 * self.relWidth)
            drawingX += 0.05 * self.boxWidth
            
            fill(0)
            textSize(20)
            relXText(self.parameterList[i].name, drawingX, self.relY + 1.06 * self.relHeight)
            drawingX += keyWidth
            
        
        # Move drawing point back to the beginning
        self.x = 0
        
        self.oldX = [None for i in self.parameterList]
        self.oldY = [None for i in self.parameterList]
    
    def update(self):
        strokeWeight(3)
        for count in range(len(self.parameterList)):
            param = self.parameterList[count]
            colour = self.colourList[count]
            stroke(colour)
            pointX = self.x + self.relX
            if self.minY <= param.value <= self.maxY:
                pointY = - self.scalingY * (param.value - self.minY) + self.relY + self.relHeight
            elif self.minY > param.value:
                pointY = self.relY + self.relHeight
            else:
                pointY = self.relY
            if self.x != 0:
                relXLine(self.oldX[count], self.oldY[count], pointX, pointY)
            self.oldX[count] = pointX
            self.oldY[count] = pointY
        strokeWeight(1)
        self.x += self.incrementX
        
        if self.x > self.relWidth:
            self.display()
    