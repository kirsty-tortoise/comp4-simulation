# TODO:
#    Implement changing screen size? Or full screen?

from Simulations import *
from RelativeDrawing import *

# Defines colours needed in the simulation.
black = color(0, 0, 0)
white = color(255, 255, 255)
red = color(255, 0, 0)
green = color(68, 247, 10)
blue = color(10, 187, 247)
orange = color(247, 192, 10)
yellow = color(247, 247, 10)

# Defines the names of the simulations, their relative positions on the screens and colours
simulationNames = ["Horizontal Circles - Coins on Roundabouts", 
                   "Horizontal Circles - Cars on a banked racetrack",
                   "Vertical Circles - Spinning beads on strings, rods and surfaces",
                   "Simple Harmonic Motion - Energy in a spring",
                   "Quit"]

optionPositions = [(0.1, 0.4, 0.8, 0.08),
                   (0.1, 0.5, 0.8, 0.08),
                   (0.1, 0.6, 0.8, 0.08),
                   (0.1, 0.7, 0.8, 0.08),
                   (0.1, 0.8, 0.8, 0.08)]

optionColours = [red, orange, yellow, green, blue]

homeButtonPosition = (0.02, 0.01, 0.04, 0.08)

simulationPlaying = False

def setup():
    '''
    Sets up the screen and displays start menu.
    '''
    size(1900, 950)
    drawHomeScreen()
    

def draw():
    '''
    Runs the simulation if one is currently being played.
    '''
    if simulationPlaying:
        simulation.updateSimulation()
        simulation.drawSimulation()
        drawHomeButton()
            
def mouseClicked():
    '''
    When the mouse is clicked, it updates the simulations if one is playing.
    If the home button is clicked, it exits to the menu screen.
    If a simulation is chosen, that simulation starts playing. 
    '''
    global simulationPlaying
    global simulation
    if simulationPlaying:
        simulation.updateMouse()
        if relIsOver(*homeButtonPosition): # *homeButtonPosition should turn a tuple into just some numbers to feed into the function
            del simulation
            simulationPlaying = False
            drawHomeScreen()
    else:
        for buttonIndex in range(len(simulationNames)):
            if relIsOver(*optionPositions[buttonIndex]):
                background(255)
                simulationToOpen = simulationNames[buttonIndex]
                if simulationToOpen == "Horizontal Circles - Coins on Roundabouts":
                    simulation = CoinOnRoundabout()
                elif simulationToOpen == "Horizontal Circles - Cars on a banked racetrack":
                    simulation = CarOnRacetrack()
                elif simulationToOpen == "Vertical Circles - Spinning beads on strings, rods and surfaces":
                    simulation = VerticalRotation()
                elif simulationToOpen == "Simple Harmonic Motion - Energy in a spring":
                    simulation = SimpleHarmonicSprings()
                elif simulationToOpen == "Quit":
                    exit()
                simulationPlaying = True
        
def keyReleased():
    '''
    If a key is pressed, it lets the simulation being played know and update itself accordingly.
    '''
    if simulationPlaying:
        simulation.pressKeys()
        
def drawHomeButton():
    '''
    Draws the home button to the top of the screen for playing simulations.
    '''
    stroke(0)
    fill(red)
    relRect(*homeButtonPosition)
    fill(blue)
    relRect(0.03, 0.04, 0.02, 0.04)
    fill(green)
    relTriangle(0.03, 0.04, 0.05, 0.04, 0.04, 0.02)
    
def drawSimulationOption(name, optionPosition, colour):
    '''
    Displays the simulation button to choose when the simulation is not playing.
    '''
    noStroke()
    fill(colour)
    relRect(* optionPosition + (7,))
    fill(black)
    textSize(50)
    textAlign(LEFT, CENTER)
    relText(name, *optionPosition + (0.015, ))

def drawHomeScreen():
    '''
    Draws all the menu options and the rest of the home screen.
    '''
    background(0)
    
    fill(255)
    textSize(100)
    textAlign(CENTER, CENTER)
    relText("M3 SIMULATIONS", 0.1, 0.1, 0.8, 0.2)
        
    for name, pos, col in zip(simulationNames, optionPositions, optionColours):
        drawSimulationOption(name, pos, col)