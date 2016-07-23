# TODO:
    
from RelativeDrawing import *

class StartStopButton(object):
    '''
    Adds the start or stop button to the screen and detects when it is pressed.
    '''
    def __init__(self, relX, relY, relWidth, relHeight):
        self.playing = False
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
    
    def display(self):
        if self.playing:
            # Draw stop button
            noStroke()
            fill(255, 0, 0)
            relXRect(self.relX, self.relY, self.relWidth, self.relHeight, 20)
            fill(0, 0, 0)
            textSize(30)
            relXText("  STOP", self.relX, self.relY, self.relWidth, self.relHeight) # Indented to centre a bit more
        else:
            # Draw start button
            noStroke()
            fill(0, 255, 0)
            relXRect(self.relX, self.relY, self.relWidth, self.relHeight, 20)
            fill(0, 0, 0)
            textSize(30)
            relXText("  START", self.relX, self.relY, self.relWidth, self.relHeight) # Indented to centre a bit more
    
    def isOver(self):
        return relXIsOver(self.relX, self.relY, self.relWidth, self.relHeight)

class ResetButton(object):
    '''
    Adds a reset button to the screen.
    '''
    def __init__(self, relX, relY, relWidth, relHeight):
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
    
    def display(self):
         noStroke()
         fill(102, 204, 255) # Blue button
         relXRect(self.relX, self.relY, self.relWidth, self.relHeight, 20)
         fill(0, 0, 0)
         textSize(30)
         relXText("  RESET", self.relX, self.relY, self.relWidth, self.relHeight) # Indented to centre a bit more
    
    def isOver(self):
        return relXIsOver(self.relX, self.relY, self.relWidth, self.relHeight)
    

class Tabs(object):
    '''
    Gives tabs to choose between for the graphs.
    '''
    def __init__(self, possibilities, relX = 0.5, relY = 0.0, relWidth = 0.5, relHeight = 0.03, selectedFill = color(0, 0, 255), unselectedFill = color(100, 200, 255), textColour = color(0)):
        '''
        Given a list of required tab names, create these tabs.
        '''
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        
        # Set up the tabs
        self.numberOfTabs = len(possibilities)
        self.tabs = []
        tabLength = relWidth / self.numberOfTabs
        currentX = relX
        for option in possibilities:
            self.tabs.append(Tab(option, currentX, relY, tabLength, relHeight, selectedFill, unselectedFill, textColour)) 
            currentX += tabLength
            
        self.currentChoiceIndex = 0
        self.currentChoice = self.tabs[0].name
        self.tabs[0].selected = True
        
        self.changed = False
    
    def updateMouse(self):
        '''
        Update for a mouse click. Checks if any of the tabs are selected, and if so, changes the selected tab.
        '''
        self.changed = False
        for t in range(self.numberOfTabs):
            tab = self.tabs[t]
            if tab.isOver():
                self.changed = True
                self.tabs[self.currentChoiceIndex].selected = False # Unselect the current tab
                tab.selected = True
                self.currentChoiceIndex = t
                self.currentChoice = tab.name
                
    def display(self):
        for tab in self.tabs:
            tab.display()        

class Tab(object):
    '''
    Implements one of the tabs to choose which graph you want.
    '''
    def __init__(self, name, relX, relY, relWidth, relHeight, selectedFill, unselectedFill, textColour):
        '''
        Sets up a tab with its size and value.
        '''
        self.name = name
        
        # Set up drawing options
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        
        self.selectedFill = selectedFill
        self.unselectedFill = unselectedFill
        self.textColour = textColour
        
        # Tabs are initially unselected
        self.selected = False
        
    def isOver(self):
        return relXIsOver(self.relX, self.relY, self.relWidth, self.relHeight)
    
    def display(self):
        if self.selected:
            fill(self.selectedFill)
        else:
            fill(self.unselectedFill)
        stroke(0) # Black stroke
        
        # Draw the surrounding box
        relXRect(self.relX, self.relY, self.relWidth, self.relHeight)
        
        # Draw the text
        fill(self.textColour)
        textSize(30)
        textAlign(CENTER, CENTER)
        relXText(self.name, self.relX, self.relY, self.relWidth, self.relHeight)
        textAlign(LEFT, UP)