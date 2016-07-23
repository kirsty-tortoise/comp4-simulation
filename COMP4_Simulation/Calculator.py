# TODO
#    Implement a basic calculator and scientific calculator.
#    Add a new ANS button
#    Change display to reset after an answer is shown.
#    Fix text settings.

import math

black = color(0, 0, 0)
white = color(255, 255, 255)

class Calculator(object):
    def __init__(self, calcX, calcY, calcWidth, calcHeight, buttons, colour):
        self.calcX = calcX
        self.calcY = calcY
        self.calcWidth = calcWidth
        self.calcHeight = calcHeight
        self.buttons = buttons
        self.ans = None
        self.current = ""
        self.display = ""
        self.colour = colour
        self.currentlyOperating = False
        self.operator = None

    def calcPressed(self):
        for button in self.buttons:
            if button.isOver(self.calcX, self.calcY, self.calcWidth, self.calcHeight):
                button.buttonPressed(self)
    
    def drawCalc(self):
        fill(self.colour)
        rect(self.calcX, self.calcY, self.calcWidth, self.calcHeight, 10)
        for button in self.buttons:
            button.drawButton(self.calcX, self.calcY, self.calcWidth, self.calcHeight)
        fill(black)
        rect(self.calcX + 0.05 * self.calcWidth, self.calcY + 0.05 * self.calcHeight , self.calcWidth * 0.9, self.calcHeight * 0.1)
        fill(white)
        textAlign(LEFT, CENTER)
        textSize(20) # Fix to make size relative to box
        text(self.display, self.calcX + 0.05 * self.calcWidth, self.calcY + 0.05 * self.calcHeight , self.calcWidth * 0.9, self.calcHeight * 0.1)
    
    
    
    
class Button(object):
    def __init__(self, relX, relY, relHeight, relWidth, label, colour):
        self.relX = relX
        self.relY = relY
        self.relHeight = relHeight
        self.relWidth = relWidth
        self.label = label
        self.colour = colour
    
    def drawButton(self, calcX, calcY, calcWidth, calcHeight):
        fill(self.colour)
        rect(calcX + self.relX * calcWidth, calcY + self.relY * calcHeight, self.relWidth * calcWidth, self.relHeight * calcHeight, 10)
        fill(black)
        textAlign(CENTER, CENTER)
        textSize(30) # FIX THIS!
        text(self.label, calcX + self.relX * calcWidth, calcY + self.relY * calcHeight, self.relWidth * calcWidth, self.relHeight * calcHeight)
    
    def isOver(self, calcX, calcY, calcWidth, calcHeight):
        return (calcX + calcWidth * self.relX <= mouseX <= calcX + calcWidth * self.relX + calcWidth * self.relWidth 
            and calcY + calcHeight * self.relY <= mouseY <= calcY + calcHeight * self.relY + calcHeight * self.relHeight)
    
    def buttonPressed(self, calculator):
        pass
    
class NumberButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, label, colour, value):
        Button.__init__(self, relX, relY, relHeight, relWidth, label, colour)
        self.value = value
    
    def buttonPressed(self, calculator):
        calculator.current += str(self.value)
        calculator.display += str(self.value)
        
class EqualsButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, colour):
        Button.__init__(self, relX, relY, relHeight, relWidth, "=", colour)
    
    def buttonPressed(self, calculator):
        if calculator.currentlyOperating:
            calculator.ans = calculator.operator.apply(calculator.ans, float(calculator.current))
            calculator.currentlyOperating = False
            calculator.current = str(calculator.ans)
        calculator.display = calculator.current
    
class FunctionButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, label, colour, function):
        Button.__init__(self, relX, relY, relHeight, relWidth, label, colour)
        self.function = function
    
    def buttonPressed(self, calculator):
        if calculator.currentlyOperating:
            calculator.ans = calculator.operator.apply(calculator.ans, float(calculator.current))
            calculator.currentlyOperating = False
        else:
            calculator.ans = float(calculator.current)
        calculator.current = self.function(calculator.ans)
        calculator.ans = calculator.current


class OperatorButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, label, colour, operator):
        Button.__init__(self, relX, relY, relHeight, relWidth, label, colour)
        self.operator = operator
    
    def buttonPressed(self, calculator):
        if calculator.currentlyOperating:
            calculator.ans = calculator.operator.apply(calculator.ans, float(calculator.current))
        else:
            calculator.ans = float(calculator.current)
        calculator.current = ""
        calculator.operator = self.operator
        calculator.currentlyOperating = True
        calculator.display += self.label

class MemoryAddButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, memorySpace, colour):
        Button.__init__(self, relX, relY, relHeight, relWidth, memorySpace.name, colour)
        self.memorySpace = memorySpace
    
    def buttonPressed(self, calculator):
        self.memorySpace.value = self.current


class MemoryCallButton(Button):
    def __init__(self, relX, relY, relHeight, relWidth, memorySpace, colour):
        Button.__init__(self, relX, relY, relHeight, relWidth, memorySpace.name, colour)
        self.memorySpace = memorySpace
    
    def buttonPressed(self, calculator):
        self.current = self.memorySpace.value
        self.display = self.memorySpace.name

class ResetButton(Button):
    def buttonPressed(self, calculator):
        calculator.current = ""
        calculator.display = ""
        calculator.ans = None

class Operator(object):
    def __init__(self, apply):
        self.apply = apply

class MemorySpace(object):
    def __init__(self, name):
        self.value = None
        self.name = name