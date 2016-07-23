# TODO:

from Parameters import *
from PhysicalObjects import *
from Extra import *
from Graphs import Graph
from ForceDiagrams import ForceDiagram

g = 9.8

class SimulationScreen(object):
    '''
    Implements a base class for all simulations to inherit from.
    '''

    def __init__(self, sliderArray, inputBoxArray, objectArray, parameterArray, rightPanelArray):
        '''
        Sets up a general based on the objects it contains.
        '''
        self.sliderArray = sliderArray
        self.inputBoxArray = inputBoxArray
        self.objectArray = objectArray
        self.rightPanelArray = rightPanelArray
        if len(rightPanelArray) != 0:
            self.currentRightPanel = rightPanelArray[0]
            self.currentRightPanel.display()
            self.rightPanelTabs = Tabs([rightPanel.name for rightPanel in rightPanelArray])
            self.rightPanelTabs.display()
        else:
            self.currentRightPanel = None
            self.rightPanelTabs = None

        self.playing = False
        self.parameterArray = parameterArray
        self.lastTime = millis()
        self.startButton = StartStopButton(0.9, 0.36, 0.08, 0.05)
        self.resetButton = ResetButton(0.9, 0.42, 0.08, 0.05)
        self.paused = False

        self.timeModeButtons = VerticalRadioButtons(["Real Time", "Controlled Time", "Slow Time"], 0.78, 0.38, 0.01)
        self.timeMode = "REALTIME"

    def updateSimulation(self):
        '''
        Updates all the objects in the simulation.
        '''

        # Update the graph currently being displayed
        if self.playing and not self.paused:
            if self.currentRightPanel:
                self.currentRightPanel.update()

        # Finally, update the sliders.
        self.updateSliders()

    def updateSliders(self):
        '''
        Updates sliders to check for input.
        '''
        for slider in self.sliderArray:
            slider.update(self.sliderArray)

    def updateMouse(self):
        '''
        Updates the simulation when clicked.
        '''
        for inputBox in self.inputBoxArray:
            inputBox.updateMouse(self.inputBoxArray)

        if self.startButton.isOver():
            self.playing = not self.playing # Change whether it is playing
            self.startButton.playing = not self.startButton.playing
            self.paused = False

        if self.resetButton.isOver():
            self.resetSimulation()
            self.paused = False

        if self.rightPanelTabs:
            self.rightPanelTabs.updateMouse()
            if self.rightPanelTabs.changed: # The graph has been changed
                self.currentRightPanel = self.rightPanelArray[self.rightPanelTabs.currentChoiceIndex]
                self.currentRightPanel.display()
                self.rightPanelTabs.display()

        self.timeModeButtons.updateMouse([]) # Empty list because it is like any other input buttons and needs to know which other input buttons it might need to interact with.
        if self.timeModeButtons.changed: # Something changed!
            #print "CHANGE!"
            if self.timeModeButtons.selected == "Real Time":
                self.timeMode = "REALTIME"
            elif self.timeModeButtons.selected == "Controlled Time":
                self.timeMode = "MEDIUMTIME"
            else:
                self.timeMode = "SLOWTIME"

    def drawSimulation(self):
        '''
        Displays all objects in the simulation to the screen.
        '''
        # Draw the top left in white.
        fill(255)
        stroke(255)
        relXRect(0, 0, 0.5, 0.35)

        # Draw the bottom of the screen in black.
        fill(0)
        stroke(0)
        relXRect(0, 0.35, 1.0, 0.15)

        # Draw all the objects
        for object in self.objectArray:
            object.display()

        # Draw all the sliders
        for slider in self.sliderArray:
            slider.drawInput()

        # And then draw all the input boxes
        for inputBox in self.inputBoxArray:
            inputBox.drawInput()

        self.timeModeButtons.drawInput()

        # Draw the start and reset buttons
        self.startButton.display()
        self.resetButton.display()

    def saveSimulation(self, fileName):
        '''
        Saves the values of the parameters to a text file.
        '''
        saveList = []
        for param in self.parameterArray:
            saveList.append(param.name + " " + str(param.value))
        saveStrings(fileName, saveList)

    def loadSimulation(self, fileName):
        '''
        Loads the values of the parameters from a text file.
        '''
        self.resetSimulation() # Makes sure everything from previous screen is back to normal.
        loadList = loadStrings(filename)
        loadDict = {}
        for param in loadList:
            p = param.split(" ")
            loadDict[p[0]] = p[1]
        for param in self.parameterArray:
            param.value = float(loadDict[param.name])

    def resetSimulation(self):
        '''
        Resets the simulation back to its original state.
        '''

        for parameter in self.parameterArray:
            parameter.initialise()

        for object in self.objectArray:
            object.initialise()

        self.playing = False
        self.startButton.playing = False

        if self.currentRightPanel:
            self.currentRightPanel.display()
            self.rightPanelTabs.display()

    def pressKeys(self):
        '''
        Checks whether any of the input boxes need the key the user has pressed, and uses it there
        '''
        for inputBox in self.inputBoxArray:
            inputBox.updateKeyboard()

    def updateTime(self):
        #print self.timeMode
        if self.timeMode == "REALTIME":
            self.deltaTime = (millis() - self.lastTime) / 1000.0
        elif self.timeMode == "MEDIUMTIME":
            self.deltaTime = 0.03
        elif self.timeMode == "SLOWTIME":
            self.deltaTime = 0.01

        self.lastTime = millis()

class CoinOnRoundabout(SimulationScreen):
    '''
    This class implements the first simulation: Horizontal circles, coins on roundabouts.
    '''

    def __init__(self):
        '''
        Sets up the simulation, requiring no inputs.
        '''
        self.omegaP = Parameter("omega", 1.0, [])
        omegaSlider = Slider(0.01, 0.37, 0.0, 10.0, "Omega", "rad/s", self.omegaP)
        omegaInputBox = InputBox(0.16, 0.36, 0.0, 10.0, self.omegaP)
        self.omegaP.inputs = [omegaSlider, omegaInputBox]

        self.massP = Parameter("mass", 5.0, [])
        massSlider = Slider(0.01, 0.43, 1.0, 10.0, "Mass", "kg", self.massP)
        massInputBox = InputBox(0.16, 0.42, 1.0, 10.0, self.massP)
        self.massP.inputs = [massSlider, massInputBox]

        self.muP = Parameter("mu", 0.5, [])
        muSlider = Slider(0.38, 0.37, 0.0, 2.0, "Coefficient of friction", "", self.muP)
        muInputBox = InputBox(0.53, 0.36, 0.0, 2.0, self.muP)
        self.muP.inputs = [muSlider, muInputBox]

        self.radiusP = Parameter("radius", 0.5, [])
        radiusSlider = Slider(0.38, 0.43, 0.01, 1.0, "Radius", "m", self.radiusP) # Minimum is 0.01 to avoid dividing by 0.
        radiusInputBox = InputBox(0.53, 0.42, 0.01, 1.0, self.radiusP)
        self.radiusP.inputs = [radiusSlider, radiusInputBox]

        sliderArray = [massSlider, omegaSlider, muSlider, radiusSlider]
        inputBoxArray = [massInputBox, omegaInputBox, muInputBox, radiusInputBox]
        parameterArray = [self.massP, self.omegaP, self.muP, self.radiusP]

        self.scaling = 0.15
        centre = Vector(1.4, 1.0)

        positionYP = Parameter("Y position", 0, [])
        positionXP = Parameter("X position", 0, [])

        self.coin = Coin(1, Vector(0, 0), Vector(0, -2), self.scaling, 0.2, 0.2, yellow, self.massP, self.radiusP, self.muP, self.omegaP, positionXP, positionYP, centre)
        self.roundabout = Roundabout(self.omegaP, centre, 2.0, self.scaling)

        coinForceDiagram = ForceDiagram("Force Diagram", "assets/CoinDiagram.png")
        projectedPositionGraph = Graph("Projected to 1D", [positionXP, positionYP], [color(0, 255, 0), color(0, 0, 255)], -1.0, 1.0)

        rightPanelArray = [coinForceDiagram, projectedPositionGraph]
        objectArray = [self.roundabout, self.coin]

        SimulationScreen.__init__(self, sliderArray, inputBoxArray, objectArray, parameterArray, rightPanelArray)

    def updateSimulation(self):
        self.updateTime()

        if self.playing:
            self.coin.update(self.coin.findForce(), self.deltaTime)
            self.roundabout.update(self.deltaTime)
            if abs(self.coin.centre - self.coin.position) > 1.2:
                self.playing = False
        else:
            self.coin.updateFromInput()
        SimulationScreen.updateSimulation(self)

class CarOnRacetrack(SimulationScreen):
    '''
    This class implements the second simulation: Horizontal circles, car on a banked racetrack.
    '''

    def __init__(self):
        '''
        Sets up the simulation, requiring no inputs.
        '''
        self.playing = False

        self.angleP = Parameter("angle", 30.0, [])
        angleSlider = Slider(0.01, 0.39, 0.0, 85.0, "Angle", "degrees", self.angleP)
        angleInputBox = InputBox(0.16, 0.38, 0.0, 85.0, self.angleP)
        self.angleP.inputs = [angleSlider, angleInputBox]

        self.massP = Parameter("mass", 1000.0, [])
        massSlider = Slider(0.01, 0.45, 0.0, 5000.0, "Mass", "kg", self.massP)
        massInputBox = InputBox(0.16, 0.44, 0.0, 5000.0, self.massP)
        self.massP.inputs = [massSlider, massInputBox]

        self.radiusP = Parameter("radius", 10.0, [])
        radiusSlider = Slider(0.38, 0.37, 2.0, 20.0, "Radius", "m", self.radiusP)
        radiusInputBox = InputBox(0.53, 0.36, 2.0, 20.0, self.radiusP)
        self.radiusP.inputs = [radiusSlider, radiusInputBox]

        self.muP = Parameter("mu", 0.5, [])
        muSlider = Slider(0.38, 0.42, 0.0, 2.0, "Coefficient of Friction", "", self.muP)
        muInputBox = InputBox(0.53, 0.41, 0.0, 2.0, self.muP)
        self.muP.inputs = [muSlider, muInputBox]

        self.speedP = Parameter("speed", 10.0, [])
        speedSlider = Slider(0.38, 0.465, 0.0, 40.0, "Speed", "m/s", self.speedP)
        speedInputBox = InputBox(0.53, 0.455,0.0, 40.0, self.speedP)
        self.speedP.inputs = [speedSlider, speedInputBox]

        self.scaling = 0.006
        self.centre = Vector(25.0, 25.0)
        self.racetrack = Racetrack(self.radiusP, 4, self.centre, self.scaling)
        self.car = Car(self.centre, self.speedP, self.radiusP, self.massP, self.angleP, self.muP, 3.0, 2.0, color(50, 100, 255), self.scaling) # Blue car
        self.breakDownMessage = BreakDownMessage("", 0.1, 0.25, 0.3, 0.1, 30)

        flyingOffUnresolved = ForceDiagram("Flying Off", "assets/CarDiagramUpSlope.png")
        flyingOffResolved = ForceDiagram("Resolved", "assets/CarDiagramResolvedUpSlope.png")
        fallingInUnresolved = ForceDiagram("Falling In", "assets/CarDiagramDownSlope.png")
        fallingInResolved = ForceDiagram("Resolved", "assets/CarDiagramResolvedDownSlope.png")


        sliderArray = [massSlider, angleSlider, muSlider, radiusSlider, speedSlider]
        inputBoxArray = [massInputBox, angleInputBox, muInputBox, radiusInputBox, speedInputBox]
        parameterArray = [self.angleP, self.massP, self.radiusP, self.muP, self.speedP]
        objectArray = [self.racetrack, self.car, self.breakDownMessage]
        rightPanelArray = [flyingOffUnresolved, flyingOffResolved, fallingInUnresolved, fallingInResolved]

        SimulationScreen.__init__(self, sliderArray, inputBoxArray, objectArray, parameterArray, rightPanelArray)

    def updateSimulation(self):
        self.updateTime()
        self.racetrack.updateFromInput()

        if self.playing:
            self.car.update(self.deltaTime)
            if self.car.slipping > 0:
                self.breakDownMessage.displayText = "The car flew off."
            elif self.car.slipping < 0:
                self.breakDownMessage.displayText = "The car fell in."
            if abs(self.car.slipped) > 2.0:
                # Stop the simulation when the car has slipped too much.
                self.playing = False
        else:
            self.car.updateFromInput()

        SimulationScreen.updateSimulation(self)


class VerticalRotation(SimulationScreen):
    '''
    This class implements the third simulation: Vertical circles
    '''

    def __init__(self):
        '''
        Sets up the simulation, requiring no inputs.
        '''
        self.radiusP = Parameter("radius", 1.5, [])
        radiusSlider = Slider(0.01, 0.37, 0.5, 2.0, "Radius", "m", self.radiusP)
        radiusInputBox = InputBox(0.16, 0.36, 0.5, 2.0, self.radiusP)
        self.radiusP.inputs = [radiusSlider, radiusInputBox]

        self.massP = Parameter("mass", 5.0, [])
        massSlider = Slider(0.01, 0.43, 1.0, 10.0, "Mass", "kg", self.massP)
        massInputBox = InputBox(0.16, 0.42, 1.0, 10.0, self.massP)
        self.massP.inputs = [massSlider, massInputBox]

        self.initialAngleP = Parameter("angle", 45.0, [])
        initialAngleSlider = Slider(0.38, 0.37, 0, 360, "Initial angle", "degrees", self.initialAngleP)
        initialAngleInputBox = InputBox(0.53, 0.36, 0, 360, self.initialAngleP)
        self.initialAngleP.inputs = [initialAngleSlider, initialAngleInputBox]

        self.initialSpeedP = Parameter("speed", 0.0, [])
        initialSpeedSlider = Slider(0.38, 0.43, 0.0, 10.0, "Initial speed", "m/s", self.initialSpeedP)
        initialSpeedInputBox = InputBox(0.53, 0.42, 0.0, 10.0, self.initialSpeedP)
        self.initialSpeedP.inputs = [initialSpeedSlider, initialSpeedInputBox]

        # Set up radio buttons
        self.modeButtons = HorizontalRadioButtons(["String", "Wire", "Outside Sphere", "Inside Sphere"], 0.05, 0.32, 0.01)

        gravitationalEnergyP = Parameter("Gravitational Potential Energy", 0, [])
        kineticEnergyP = Parameter("Kinetic Energy", 0, [])

        generalForceDiagram = ForceDiagram("Force Diagram", "assets/VerticalCirclesForces.png")
        energyGraph = Graph("Energy", [gravitationalEnergyP, kineticEnergyP], [color(255, 255, 0), color(155, 0, 255)], -400, 400)

        sliderArray = [massSlider, initialAngleSlider, initialSpeedSlider, radiusSlider]
        inputBoxArray = [massInputBox, initialAngleInputBox, initialSpeedInputBox, radiusInputBox, self.modeButtons]
        parameterArray = [self.radiusP, self.massP, self.initialAngleP, self.initialSpeedP]

        self.scaling = 0.06
        self.centre = Vector(2.6, 2.4)
        self.mass = CircularMass(0.1, Vector(0, 0), Vector(0, 0), self.scaling, color(0, 0, 0), self.massP, self.radiusP, self.initialAngleP, self.initialSpeedP,
                                 kineticEnergyP, gravitationalEnergyP, self.centre)
        self.breakDownMessage = BreakDownMessage("", 0.1, 0.23, 0.3, 0.1, 30)

        objectArray = [None, self.mass, self.breakDownMessage] # None place holds for the circle thing
        rightPanelArray = [generalForceDiagram, energyGraph]
        SimulationScreen.__init__(self, sliderArray, inputBoxArray, objectArray, parameterArray, rightPanelArray)

        self.mode = "String"
        self.setUpCircle()
        self.paused = False

    def updateSimulation(self):
        self.updateTime()

        if self.mode != self.modeButtons.selected:
            self.mode = self.modeButtons.selected
            self.setUpCircle()

        if self.playing and not self.paused:
            forceRequired = self.mass.forceInwardsRequired()
            if self.circleThing.checkForceInwards(forceRequired):
                self.mass.update(Vector(0, self.mass.mass * g) + (self.centre - self.mass.position).scaleAbs(forceRequired), self.deltaTime)
            else:
                self.paused = True
                # Choose appropriate error message.
                if self.mode == "String":
                    self.breakDownMessage.displayText = "The string became slack."
                elif self.mode == "Outside Sphere":
                    self.breakDownMessage.displayText = "The mass fell off the sphere."
                elif self.mode == "Inside Sphere":
                    self.breakDownMessage.displayText = "The mass fell inside the sphere."

            self.circleThing.updateFromInput()
        elif not self.paused:
            self.breakDownMessage.displayText = ""
            self.mass.updateWhenPaused()
            self.circleThing.updateFromInput()

        SimulationScreen.updateSimulation(self)

    def setUpCircle(self):
        if self.mode == "String":
            self.circleThing = Rope(self.mass, self.centre, self.scaling)
        elif self.mode == "Wire":
            self.circleThing = Wire(self.mass, self.centre, self.scaling)
        elif self.mode == "Outside Sphere":
            self.circleThing = OutsideSphere(self.radiusP, self.centre, self.scaling, color(154, 10, 207), color(218, 124, 252, 20))
        elif self.mode == "Inside Sphere":
            self.circleThing = InsideSphere(self.radiusP, self.centre, self.scaling, color(154, 10, 207), color(218, 124, 252, 20))
        self.objectArray[0] = self.circleThing # Swap it into the object list.

class SimpleHarmonicSprings(SimulationScreen):
    '''
    This class implements the fourth simulation: Simple Harmonic Motion, Energy in a spring.
    '''

    def __init__(self):
        '''
        Sets up the simulation, requiring no inputs.
        '''
        # First, set up all input parameters and input sliders / boxes
        self.numberOfMassesP = Parameter("masses", 1, [])
        massSlider = IntSlider(0.01, 0.37, 1.0, 5.0, "Number Of Masses", "", self.numberOfMassesP)
        massInputBox = IntInputBox(0.16, 0.36, 1.0, 5.0, self.numberOfMassesP)
        self.numberOfMassesP.inputs = [massSlider, massInputBox]

        self.stiffnessP = Parameter("stiffness", 50.0, [])
        stiffnessSlider = Slider(0.01, 0.43, 1.0, 100.0, "Stiffness Constant", "N/m", self.stiffnessP)
        stiffnessInputBox = InputBox(0.16, 0.42, 1.0, 100.0, self.stiffnessP)
        self.stiffnessP.inputs = [stiffnessSlider, stiffnessInputBox]

        self.naturalLengthP = Parameter("naturallength", 1.0, [])
        naturalLengthSlider = Slider(0.38, 0.37, 0.5, 3.0, "Natural Length", "m", self.naturalLengthP)
        naturalLengthInputBox = InputBox(0.53, 0.36, 0.5, 3.0, self.naturalLengthP)
        self.naturalLengthP.inputs = [naturalLengthSlider, naturalLengthInputBox]

        self.originalDisplacementP = Parameter("displacment", 0.0, [])
        originalDisplacementSlider = Slider(0.38, 0.43, -1.0, 1.0, "Original Displacement", "m", self.originalDisplacementP)
        originalDisplacementInputBox = InputBox(0.53, 0.42, -1.0, 1.0, self.originalDisplacementP)
        self.originalDisplacementP.inputs = [originalDisplacementSlider, originalDisplacementInputBox]

        sliderArray = [massSlider, stiffnessSlider, naturalLengthSlider, originalDisplacementSlider]
        inputBoxArray = [massInputBox, stiffnessInputBox, naturalLengthInputBox, originalDisplacementInputBox]

        # Now set up output parameters
        self.tensionP = Parameter("Tension", 0, [])
        elasticEnergyP = Parameter("Elastic Energy", 0, [])
        kineticEnergyP = Parameter("Kinetic Energy", 0, [])
        displacementP = Parameter("Displacement", 0, [])
        velocityP = Parameter("Velocity", 0, [])
        accelerationP = Parameter("Acceleration", 0, [])

        # Now set up the actual springs and masses
        scaling = 0.1
        massRelWidth = 0.3
        massRelHeight = 0.1
        self.springX = 2.0
        self.spring = Spring(self.naturalLengthP, self.stiffnessP, 20, self.originalDisplacementP, self.springX, 0.5, scaling, self.tensionP, elasticEnergyP, 0.05)
        self.springMass = Mass(Vector(self.springX, 1 + self.naturalLengthP.value), Vector(0, 0), self.numberOfMassesP, kineticEnergyP, displacementP, velocityP, accelerationP, scaling, massRelWidth, massRelHeight, black, red)

        energyGraph = Graph("Energy", [elasticEnergyP, kineticEnergyP], [color(0), color(0, 255, 0)], 0, 30)
        motionGraph = Graph("Motion", [displacementP, velocityP, accelerationP], [color(0), color(0, 255, 0), color(0, 0, 255)], -20, 20)

        rightPanelArray = [energyGraph, motionGraph]
        parameterArray = [self.numberOfMassesP, self.stiffnessP, self.naturalLengthP, self.originalDisplacementP]
        objectArray = [self.spring, self.springMass]
        SimulationScreen.__init__(self, sliderArray, inputBoxArray, objectArray, parameterArray, rightPanelArray)

    def updateSimulation(self):
        self.updateTime()

        if self.playing:
            self.springMass.update(Vector(0.0,  -self.tensionP.value + g * self.springMass.mass), self.deltaTime)
            self.spring.update(self.springMass.position.y)
        else:
            self.spring.update()
            self.springMass.update(bottom = Vector(self.springX, 0.5 + self.naturalLengthP.value + self.originalDisplacementP.value + 3 * self.spring.radius))

        SimulationScreen.updateSimulation(self)
