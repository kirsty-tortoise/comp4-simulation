# TODO:
#    Implement Yes/No button

from RelativeDrawing import *
from ExpressionsEvaluation import fullEvaluate

class Parameter(object):
    '''
    Implements a class that stores a value
    '''
    
    def __init__(self, name, initial, inputs):
        '''
        Initialises the object with a name, value and list of connected input boxes.
        '''
        self.name = name
        self.inputs = inputs
        self.initial = initial    
        self.setParameter(initial)   
        
    def setParameter(self, value):
        '''
        Changes the value and the value of all other inputs.
        '''
        self.value = value
        for input in self.inputs:
            input.setValue(value)
    
    def initialise(self):
        self.setParameter(self.initial)
            
class ParameterInput(object):
    '''
    Implements the base class that other inputs such as sliders inherit from.
    '''
    
    def __init__(self, relX, relY, relWidth, relHeight, label, unit, parameter):
        '''
        Sets up the extra attributes needed for any input. 
        The parameter is the parameter that needs to be updated on any change.
        '''        
        self.relX = relX
        self.relY = relY
        self.relHeight = relHeight
        self.relWidth = relWidth
        self.label = label
        self.unit = unit
        self.parameter = parameter
        self.value = self.parameter.value
        
    def setValue(self, newValue):
        '''
        Sets the value to whatever the new value is. 
        More complex methods will override this in inheriting classes.
        '''
        self.value = newValue
    
    def isOver(self):
        '''
        Checks if the mouse is over the input box.
        '''
        return self.relX <= float(mouseX) / width <= self.relX + self.relWidth and self.relY <= float(mouseY) / width <= self.relY + self.relHeight

class Slider(ParameterInput):
    '''
    Implements a slider input to the system.
    '''
    
    def __init__(self, relX, relY, starting, ending, label, unit, parameter, relLength = 0.14, relWidth = 0.01, relHeight = 0.02, colour1 = color(255, 0, 0), colour2 = color(0, 255, 0), textcolour = color(255, 255, 255)):
        '''
        Sets up a slider. 
        - relX and relY represent position of the box the slider moves along
        - relLength is the length of the box the line the slider moves along
        - relWidth and relHeight are the width and height of the actual slider that moves
        - starting and ending represent the bounds the slider can be moved between
        - initial is the value of the slider at the beginning or when reset
        - v is how far (in relative coordinates) along the slider the value is
        - colour 1 is for line and border (default red), colour 2 is for inside (default green) and text colour (default white) is for the labels.
        '''
        ParameterInput.__init__(self, relX, relY, relWidth, relHeight, label, unit, parameter)
        self.relLength = relLength
        self.starting = starting
        self.ending = ending
        self.setValue(parameter.value)
        self.colour1 = colour1
        self.colour2 = colour2
        self.textcolour = textcolour
        self.isDown = True
    
    def drawInput(self):
        '''
        Draws the slider to the screen as a line with a rectangle that moves along it.
        '''
        stroke(self.colour1)
        relXLine(self.relX, self.relY, self.relX + self.relLength, self.relY)
        fill(self.colour2)
        relXRect(self.relX + self.v - self.relWidth / 2.0, self.relY - self.relHeight / 2.0, self.relWidth, self.relHeight)
        fill(self.textcolour)
        textSize(14)
        textAlign(LEFT)
        relXText(self.label + " " + str(round(self.value, 2)) + " " + self.unit, self.relX, self.relY + self.relHeight * 1.1)
   
    def update(self, sliders):
        '''
        Whenever the system is updated, we may need to move the slider or stop moving the slider.
        On each turn:
            If the mouse is pressed:
                If the mouse if over the slider, then the slider should be down.
                If the mouse is down, then update.
            If the mouse isn't pressed, the slider shouldn't be down.
        '''
        if mousePressed:
            if self.isOver():
                # Check that no other sliders are currently down
                noneDown = True
                for slider in sliders:
                    if slider.isDown:
                        noneDown = False
                if noneDown:
                    self.isDown = True
            if self.isDown:
                self.v = min(max(mouseX / float(width), self.relX), self.relX + self.relLength) - self.relX
                self.value = self.starting + float(self.ending - self.starting) * self.v / self.relLength
                self.parameter.setParameter(self.value)
        else:
            self.isDown = False        
    
    def setValue(self, value):
        '''
        Sets a value and the position of the slider using not nice maths, if another parameter changes it.
        '''
        self.value = value
        self.v = (value - self.starting) * self.relLength / float(self.ending - self.starting)
    
    def isOver(self):
        '''
        Checks if the mouse is over the slider.
        '''
        return self.relX <= float(mouseX) / width <= self.relX + self.relLength and self.relY - 2 * self.relHeight <= float(mouseY) / width <= self.relY + self.relHeight

class IntSlider(Slider):
    def update(self, sliders):
        '''
        Updates exactly the same as before, but with a correction to the nearest integer. (done by round(int))
        '''
        if mousePressed:
            if self.isOver():
                # Check that no other sliders are currently down
                noneDown = True
                for slider in sliders:
                    if slider.isDown:
                        noneDown = False
                if noneDown:
                    self.isDown = True
            if self.isDown:
                self.v = min(max(mouseX / float(width), self.relX), self.relX + self.relLength) - self.relX
                self.value = self.starting + float(self.ending - self.starting) * self.v / self.relLength
                self.value = int(round(self.value))
                self.parameter.setParameter(self.value)
        else:
            self.isDown = False

class InputBox(ParameterInput):
    def __init__(self, relX, relY, minValue, maxValue, parameter, relWidth = 0.16,  relHeight = 0.03, writingFill = color(50, 100, 255), notWritingFill = color(100, 200, 255)):
        '''
        Sets up an input box. 
        - relX, relY, relWidth and relHeight refer to the relative positioning of the input box.
        - number refers to the unique id number of each input box in use.
        - parameter is the parameter the input box is connected to.
        - writing fill is the colour of the box when writing (default dark green) and notWritingFill is the colour of the box when not writing (default light green)
        '''
        ParameterInput.__init__(self, relX, relY, relWidth, relHeight, "", "", parameter)

        self.entry = ""
        self.writing = False
        self.writingFill = writingFill
        self.notWritingFill = notWritingFill
        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ({[]})1234567890^/*+-. " # Accepted letters
        self.checkbox = Checkbox(relX + relWidth * 1.1, relY, relHeight, relHeight)
        self.minValue = minValue
        self.maxValue = maxValue
    
    def drawInput(self):
        '''
        Draws the input box to the screen.
        '''
        # Set fill colour based on whether you are writing.
        if self.writing:
            fill(self.writingFill)
            stroke(0)
            strokeWeight(3)
        else:
            fill(self.notWritingFill)
            noStroke()
        
        # Draw the rectangle and the current entry.
        relXRect(self.relX, self.relY, self.relWidth, self.relHeight, 10)
        textAlign(LEFT, CENTER)
        textSize(20)
        fill(0)
        relXText(" " + self.entry, self.relX, self.relY, self.relWidth, self.relHeight)
        
        self.checkbox.drawCheckbox()
        
    def getInput(self):
        '''
        When a key is pressed, either add this to the entry, or take away the last digit if backspace.
        '''
        try: # Catching random keys without string conversions (most importantly shift)
            if key == "": # Check for backspaces
                self.entry = self.entry[:-1] 
            elif key == "\n":
                self.processExpression()
            elif key in self.alphabet: # Ignore input that isn't an allowed letter or number (Processing should do Shift Automatically)
                self.entry += str(key)
        except:
            pass
    
    def updateMouse(self, inputBoxes):
        '''
        Updates based on mouse clicks
        '''
        # If the mouse is pressed it is over the box, turn all other boxes off and this one on.
        if self.isOver():
             for inputbox in inputBoxes:
                 inputbox.writing = False
             self.writing = True
             self.entry = ""
     
        if self.checkbox.isOver():
             self.processExpression()
                 
    def processExpression(self):
        try:
            answer = fullEvaluate(self.entry)
            self.writing = False
            if self.minValue <= answer <= self.maxValue:
                self.parameter.setParameter(answer)
                self.entry = str(answer)
            else:
                self.entry = str(answer) + " is not in range."
    
        except:
            # Need to change to give helpful feedback!
            self.writing = False
            self.entry = "Not a valid expression."
    
    def setValue(self, newValue):
        '''
        Sets the value to whatever the new value is and clears input box.
        '''
        self.value = newValue
        self.writing = False
        self.entry = ""
                     
    def updateKeyboard(self):
       '''
       Updated based on key presses.
       '''
       if self.writing:
           self.getInput()
           
class IntInputBox(InputBox):
    '''
    Like Input Box, but rounds all non integers.
    '''
    def processExpression(self):
        try:
            answer = int(round(fullEvaluate(self.entry)))
            self.writing = False
            if self.minValue <= answer <= self.maxValue:
                self.parameter.setParameter(answer)
                self.entry = str(answer)
            else:
                self.entry = str(answer) + " is not in range."
    
        except:
            # Need to change to give helpful feedback!
            print "Oops, error in evaluation"

class Checkbox(object):
    '''
    Implements the checkboxes attached to each input box.
    '''
    
    def __init__(self, relX, relY, relWidth, relHeight, boxColour = color(30, 235, 48), tickColour = color(0, 0, 0)):
        '''
        Sets up a checkbox with the given size and box and tick colour (default green and black respectively)
        '''
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        self.boxColour = boxColour
        self.tickColour = tickColour
    
    def isOver(self):
        '''
        Checks if the mouse is over the checkbox.
        '''
        return self.relX <= float(mouseX) / width <= self.relX + self.relWidth and self.relY <= float(mouseY) / width <= self.relY + self.relHeight
    
    def drawCheckbox(self):
        '''
        Draws a box with a tick in it.
        '''
        # Draws the box
        noStroke()
        fill(self.boxColour)
        relXRect(self.relX, self.relY, self.relWidth, self.relHeight, 10)
        
        # And then draws the tick.
        stroke(self.tickColour)
        strokeWeight(5)
        relXLine(self.relX + self.relWidth * 0.2, self.relY + self.relHeight * 0.6, self.relX + self.relWidth * 0.5, self.relY + self.relHeight * 0.8)
        relXLine(self.relX + self.relWidth * 0.5, self.relY + self.relHeight * 0.8, self.relX + self.relWidth * 1.1, self.relY)
        strokeWeight(1)
        
class RadioButtons(ParameterInput):    
    def select(self, element):
        '''
        Turns on the selected radio button and turns all other buttons off.
        '''
        self.selected = element.name
        for button in self.buttons:
            button.selected = False
        element.selected = True
    
    def updateMouse(self, inputBoxes):
        '''
        Checks if the mouse is over any of the radio buttons (when clicked) and if it is then select that element.
        '''
        self.changed = False
        for button in self.buttons:
            if button.isOver():
                self.changed = True
                self.select(button)
    
    def drawInput(self):
        for button in self.buttons:
            button.drawInput()
    
    def updateKeyboard(self):
        pass

class HorizontalRadioButtons(RadioButtons):
    def __init__(self, options, relX, relY, relRadius, outerColour = color(0), innerColour = color(255), textColour = color(0)):
        self.buttons = []
        
        # Set up the option buttons horizontally
        currentX = relX
        for option in options:
            self.buttons.append(OneButton(option, currentX, relY, relRadius, outerColour, innerColour, textColour))
            currentX += 0.12
        
        self.select(self.buttons[0])
        self.changed = True

class VerticalRadioButtons(RadioButtons):
    def __init__(self, options, relX, relY, relRadius, outerColour = color(255), innerColour = color(0), textColour = color(255)):
        self.buttons = []
        
        # Set up the option buttons vertically
        currentY = relY
        for option in options:
            self.buttons.append(OneButton(option, relX, currentY, relRadius, outerColour, innerColour, textColour))
            currentY += 0.03
        
        self.select(self.buttons[0])
        self.changed = True

class OneButton(object):
    def __init__(self, name, relX, relY, relRadius, outerColour, innerColour, textColour):
        self.name = name
        self.relX = relX
        self.relY = relY
        self.relRadius = relRadius
        self.selected = False
        self.outerColour = outerColour
        self.innerColour = innerColour
        self.textColour = textColour
    
    def drawInput(self):
        # Draw the outer circle
        fill(self.innerColour)
        stroke(self.outerColour)
        strokeWeight(5)
        relXEllipse(self.relX, self.relY, 2 * self.relRadius, 2 * self.relRadius)
        
        # Draw an inner circle if selected.
        fill(self.outerColour)
        if self.selected:
            relXEllipse(self.relX, self.relY, 1.8 * self.relRadius, 1.8 * self.relRadius)
        
        # Draw the text next to it.
        fill(self.outerColour)
        strokeWeight(1)
        textSize(20)
        relXText(self.name, self.relX + 1.3 * self.relRadius, self.relY)
    
    def isOver(self):
        '''
        Checks if the mouse is over the radio button.
        '''
        return self.relX - self.relRadius <= float(mouseX) / width <= self.relX + self.relRadius and self.relY - self.relRadius <= float(mouseY) / width <= self.relY + self.relRadius
        