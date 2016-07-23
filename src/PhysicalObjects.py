# TODO:
#    Implement other objects

from Vectors import Vector
from RelativeDrawing import *

# Defines colours needed in the simulation.
black = color(0, 0, 0)
white = color(255, 255, 255)
red = color(255, 0, 0)
green = color(68, 247, 10)
blue = color(10, 187, 247)
orange = color(247, 192, 10)
yellow = color(247, 247, 10)

g = 9.8

class PhysicalObject(object):
    '''
    The base class for implementing Physical objects.
    '''
    
    def __init__(self, position, velocity, picture, scaling, relWidth, relHeight):
        '''
        Initialises a physical object. Picture should be loaded from a file, and scaling describes the relation between relative coordinates and metres.
        '''

        self.position = position
        self.velocity = velocity
        self.picture = picture
        self.scaling = scaling
        self.relWidth = relWidth
        self.relHeight = relHeight
        self.acceleration = Vector(0, 0)
        
        self.updateFromInput() # Gets mass etc. from input
        self.updateToOutput
        
    
    def update(self, force, time):
        '''
        Takes a force and a time, and updates velocity and position by one tick.
        '''
        self.updateFromInput() # Changes any attributes based on whether parameters have been changed by the user.
        
        self.acceleration = force / self.mass
        self.velocity += self.acceleration * time
        self.position += self.velocity * time
        
        self.updateFromInput() # Keep updating to make sure there are no errors.
        self.updateToOutput()
    
    def updateFromInput(self):
        '''
        This will update the appropriate things from input (such as mass parameters) if they have changed.
        The function will actually do things for specific objects.
        '''
        pass
    
    def updateToOutput(self):
        '''
        This will update any parameters we are keeping track of for graphs.
        The function will actually do things for specific objects. 
        '''
        pass
    
    def display(self):
        '''
        Draws the image to the screen at the correct relative positions.
        '''
        relXImage(self.picture, self.scaling * self.position.x, self.scaling * self.position.y, self.relWidth, self.relHeight)
    
    def initialise(self):
        '''
        For some objects, it returns it to its initial state, eg on the spring.
        '''
        pass
        
class Spring(PhysicalObject):
    '''
    A class that implements the behaviour of a spring.
    '''
    
    def __init__(self, naturalLengthP, stiffnessP, numberOfCoils, initialExtensionP, topX, topY, scaling, tensionP, elasticEnergyP, radius):
        '''
        Sets up a spring.
        Any input ending with P should be a reference to a parameter
        '''
        self.topX = topX
        self.topY = topY
        self.stiffnessP = stiffnessP
        self.initialExtensionP = initialExtensionP
        self.naturalLengthP = naturalLengthP
        self.numberOfCoils = numberOfCoils
        self.scaling = scaling
        self.tensionP = tensionP
        self.elasticEnergyP = elasticEnergyP
        self.playing = False
        self.radius = radius
        
        self.update()
    
    def update(self, bottomY = None):
        '''
        Updates the spring and any other connected parameters.
        '''
        self.naturalLength = self.naturalLengthP.value
        self.stiffness = self.stiffnessP.value
        
        if bottomY is None: # When not playing, just keep extension as its initial value.
            self.extension = self.initialExtensionP.value
            self.totalLength = self.extension + self.naturalLength
        else:
            self.totalLength = bottomY - self.topY - 3 * self.radius # There is an extra 3 * the radius in the display that isn't part of its length
            self.extension = self.totalLength - self.naturalLength
        
        # Update parameters for graphs.
        self.tensionP.setParameter(self.extension * self.stiffness)
        self.elasticEnergyP.setParameter(0.5 * self.stiffness * self.extension ** 2)
    
    def display(self):
        stroke(black) # All springs are drawn in black
        noFill()
        
        # Now adjust for the scaling of the system.
        realX = self.topX * self.scaling
        realY = self.topY * self.scaling
        realRadius = self.radius * self.scaling
        stepSize = (self.totalLength / (4.0 * self.numberOfCoils)) * self.scaling
        currentPosition = (self.topY + 2 * self.radius) * self.scaling      
        
        relXEllipse(realX, realY, 2 * realRadius, 2 * realRadius)
        relXLine(realX, realY + realRadius, realX, realY + 2 * realRadius)
        for coil in range(self.numberOfCoils):
            relXLine(realX, currentPosition, realX - realRadius, currentPosition + stepSize)
            currentPosition += stepSize
            relXLine(realX - realRadius, currentPosition, realX + realRadius, currentPosition + 2 * stepSize)
            currentPosition += 2 * stepSize
            relXLine(realX + realRadius, currentPosition, realX, currentPosition + stepSize)
            currentPosition += stepSize
        relXLine(realX, currentPosition, realX, currentPosition + realRadius)
    
    def initialise(self):
        self.velocity = Vector(0, 0)

class Mass(PhysicalObject):
    '''
    The class for the masses attached to springs.
    '''
    
    def __init__(self, position, velocity, numberOfMassesP, kineticEnergyP, displacementP, velocityP, accelerationP, scaling, relWidth, relHeight, borderColour, fillColour, massPerMass = 1.0):
        '''
        Sets up a mass (the collection). The position refers to the top centre of the masses, and the height is the height of a single mass.
        The position should currently be 3 radiuses below the topOfSpring + length + extension
        '''
        self.numberOfMassesP = numberOfMassesP
        self.kineticEnergyP = kineticEnergyP
        self.displacementP = displacementP
        self.velocityP = velocityP
        self.accelerationP = accelerationP
        self.borderColour = borderColour
        self.fillColour = fillColour
        self.massPerMass = massPerMass
        PhysicalObject.__init__(self, position, velocity, None, scaling, relWidth, relHeight)
        
    def updateFromInput(self):
        self.numberOfMasses = self.numberOfMassesP.value
        self.mass = self.massPerMass * self.numberOfMasses
    
    def display(self):
        '''
        Draws all the masses to the screen.
        '''
        fill(self.fillColour)
        stroke(self.borderColour)
        
        # Set up scaled variables for drawing
        leftSide = (self.position.x - self.relWidth / 2) * self.scaling
        currentPosition = self.position.y * self.scaling
        stepSize = self.relHeight * self.scaling
        
        for count in range(self.numberOfMasses):
            relXRect(leftSide, currentPosition, self.relWidth * self.scaling, stepSize)
            currentPosition += stepSize
    
    def update(self, force = None, time = None, bottom = None):
        '''
        If the force hasn't been supplied, move it to the bottom (if supplied).
        Else run the usual update methods.
        '''
        if force is None:
            if not bottom is None:
                self.position = bottom
            self.velocity = Vector(0, 0) # Reset the velocity to zero if is it paused or stopped.
            self.updateFromInput()
        else:
            PhysicalObject.update(self, force, time)
    
    def updateToOutput(self):
        self.kineticEnergyP.setParameter(self.mass * abs(self.velocity) ** 2)
        self.accelerationP.setParameter(self.acceleration.y)
        self.velocityP.setParameter(self.velocity.y)
        self.displacementP.setParameter(self.position.y)
        
    
class Coin(PhysicalObject):
    '''
    A class that implements the methods for drawing a coin.
    '''
    
    def __init__(self, radius, position, velocity, scaling, relWidth, relHeight, fillColour, massP, radiusP, muP, omegaP, positionXP, positionYP, centre):
        self.fillColour = fillColour
        self.radius = radius
        self.onRoundabout = True
        self.centre = centre
        self.massP = massP
        self.radiusP = radiusP
        self.muP = muP
        self.omegaP = omegaP
        self.positionXP = positionXP
        self.positionYP = positionYP
        self.initialPosition = position
        self.initialVelocity = velocity
        PhysicalObject.__init__(self, position, velocity, None, scaling, relWidth, relHeight)
    
    def display(self):
        stroke(0, 0, 0)
        fill(self.fillColour)
        relXEllipse(self.position.x * self.scaling, self.position.y * self.scaling, self.relWidth * self.scaling, self.relHeight * self.scaling)
    
    def initialise(self):
        # Just call the __init__ function to reset everything.
        self.__init__(self.radius, self.initialPosition, self.initialVelocity, self.scaling, self.relWidth, self.relHeight, self.fillColour, self.massP, self.radiusP, self.muP, self.omegaP, self.positionXP, self.positionYP, self.centre)
     
    def updateFromInput(self):
        self.mass = self.massP.value # Update mass from parameter
        
        requiredVelocity = self.omegaP.value * self.radiusP.value        
        
        if self.onRoundabout:
            # Update position and velocity from radius, only before it has slipped
            self.position = self.centre + (self.position - self.centre).scaleAbs(self.radiusP.value)
        
            self.velocity = Vector(-(self.position - self.centre).y, (self.position - self.centre).x).scaleAbs(requiredVelocity) # Always scale up the speed.
        else:
            self.velocity = self.velocity.scaleAbs(requiredVelocity)
        
        self.mu = self.muP.value
    
    def updateToOutput(self):
        self.positionXP.setParameter((self.position - self.centre).x)
        self.positionYP.setParameter((self.centre - self.position).y) # As up is negative, calculate centre - position
    
    def findForce(self):
        if self.onRoundabout and g * self.mu > self.omegaP.value ** 2 * self.radiusP.value:
            return (self.centre - self.position).scaleAbs(abs(self.velocity) ** 2 / self.radiusP.value * self.mass)
        else:
            self.onRoundabout = False
            return Vector(0, 0) # Not very realistic, but works well for demonstrations
        
class Roundabout(PhysicalObject):
    def __init__(self, omegaP, centre, radius, scaling):
        self.omegaP = omegaP
        self.centre = centre
        self.radius = radius
        self.angle = 0.0
        self.scaling = scaling
        
    def update(self, time):
        self.angle += self.omegaP.value * time
    
    def display(self):
        noStroke()
        fill(255, 14, 14)
        relXArc(self.centre.x * self.scaling, self.centre.y * self.scaling, self.radius * self.scaling, self.radius * self.scaling, self.angle, self.angle + HALF_PI)
        fill(30, 255, 14)
        relXArc(self.centre.x * self.scaling, self.centre.y * self.scaling, self.radius * self.scaling, self.radius * self.scaling, self.angle + HALF_PI, self.angle + PI)
        fill(14, 167, 255)
        relXArc(self.centre.x * self.scaling, self.centre.y * self.scaling, self.radius * self.scaling, self.radius * self.scaling, self.angle + PI, self.angle + PI * 1.5)
        fill(255, 255, 14)
        relXArc(self.centre.x * self.scaling, self.centre.y * self.scaling, self.radius * self.scaling, self.radius * self.scaling, self.angle + 1.5 * PI, self.angle + TWO_PI)
     
        
class Car(PhysicalObject):
    '''
    A class that implements methods for drawing the car.
    '''
    
    def __init__():
        pass
        
    def display():
        pass

class Rope(PhysicalObject):
    '''
    A class that implements a rope (physical string) for spinning things simulation
    '''
    
    def __init__(self, objectAttached, centre, scaling):
        self.objectAttached = objectAttached
        self.centre = centre
        self.updateFromInput()
        self.scaling = scaling
    
    def update(self):
        self.updateFromInput()
    
    def updateFromInput(self):
        self.otherEnd = self.objectAttached.position
    
    def checkForceInwards(self, forceInwards):
        '''
        Checks if the force (assumed to be inwards) is okay for the string to be exerting that force.
        '''
        if forceInwards > 0:
            return forceInwards
        else:
            return 0
            # Strings cannot return an outward force.
            
    def display(self):
        stroke(0)
        strokeWeight(3)
        relXLine(self.centre.x * self.scaling, self.centre.y * self.scaling, self.otherEnd.x * self.scaling, self.otherEnd.y * self.scaling)
        strokeWeight(1)
            
class Wire(PhysicalObject):
    def __init__(self, objectAttached, centre, scaling):
        self.objectAttached = objectAttached
        self.centre = centre
        self.updateFromInput()
        self.scaling = scaling
        
    def update(self):
        self.updateFromInput()
    
    def updateFromInput(self):
        self.otherEnd = self.objectAttached.position
    
    def checkForceInwards(self, forceInwards):
        return True # Wires can exert forces in either direction!
    
    def display(self):
        stroke(200, 200, 200)
        strokeWeight(2)
        relXLine(self.centre.x * self.scaling, self.centre.y * self.scaling, self.otherEnd.x * self.scaling, self.otherEnd.y * self.scaling)
        strokeWeight(1)

class Sphere(PhysicalObject):
    def __init__(self, radiusP, centre, scaling, strokeColour, fillColour):
        self.radiusP = radiusP
        self.centre = centre
        self.scaling = scaling
        self.updateFromInput()
        self.fillColour = fillColour
        self.strokeColour = strokeColour
    
    def update(self):
        self.updateFromInput()
    
    def display(self):
        fill(self.fillColour)
        stroke(self.strokeColour)
        relXEllipse(self.centre.x * self.scaling, self.centre.y * self.scaling, self.diameter * self.scaling, self.diameter * self.scaling)
    
class InsideSphere(Sphere):
    def updateFromInput(self):
        # As the mass is inside, the diameter needs to be slightly bigger than twice the radius of the masses orbit
        self.diameter = 2.1 * self.radiusP.value 
    
    def checkForceInwards(self, forceInwards):
        if forceInwards >= 0:
            return True
        else:
            return False # If you are inside a sphere, you can only feel a force inwards

class OutsideSphere(Sphere):
    def updateFromInput(self):
        # As the mass is outside, the diameter needs to be slightly smaller than twice the radius of the masses orbit
        self.diameter = 1.9 * self.radiusP.value 
    
    def checkForceInwards(self, forceInwards):
        if forceInwards <= 0:
            return True
        else:
            return False # If you are outside a sphere, you can only feel a force outwards from it.
        
class CircularMass(PhysicalObject):
    '''
    Implements the masses for the strings and wires simulation.
    '''
    
    def __init__(self, radius, position, velocity, scaling, fillColour, massP, radiusP, initialAngleP, initialSpeedP, kineticEnergyP, gravitationalEnergyP, centre):
        self.fillColour = fillColour
        self.radius = radius
        self.moving = True
        self.centre = centre
        self.massP = massP
        self.radiusP = radiusP
        self.initialAngleP = initialAngleP
        self.initialSpeedP = initialSpeedP
        self.kineticEnergyP = kineticEnergyP
        self.gravitationalEnergyP = gravitationalEnergyP
        self.updateWhenPaused() # Now set mass, position and velocity from parameters
        PhysicalObject.__init__(self, self.position, self.velocity, None, scaling, radius, radius)
    
    def display(self):
        stroke(0, 0, 0)
        fill(self.fillColour)
        relXEllipse(self.position.x * self.scaling, self.position.y * self.scaling, self.radius * self.scaling, self.radius * self.scaling)
        
    def updateFromInput(self):
        self.mass = self.massP.value
        self.position = self.centre + (self.position - self.centre).scaleAbs(self.radiusP.value)
        
    def updateToOutput(self):
        self.kineticEnergyP.setParameter(0.5 * self.mass * abs(self.velocity) ** 2)
        self.gravitationalEnergyP.setParameter(self.mass * g * (self.centre - self.position).y)
    
    def updateWhenPaused(self):
        self.mass = self.massP.value # Update mass from parameter
        
        # Use trig to find components
        x = self.radiusP.value * sin(radians(self.initialAngleP.value))
        y = self.radiusP.value * cos(radians(self.initialAngleP.value))
        
        self.position = self.centre + Vector(x, y)
        self.velocity = Vector(y, -x).scaleAbs(self.initialSpeedP.value)
    
    def forceInwardsRequired(self):
        '''
        Determines the inward force required from the object to stay in circular motion.
        '''
        
        self.updateFromInput() # Keeps it up to date so as to reduce rounding errors
        
        # Calculate the component of the weight inwards
        weight = self.mass * g
        fromCentre = (self.centre - self.position)
        cosAngle = fromCentre.y / abs(fromCentre)
        weightInwards = weight * cosAngle
        
        # Calculate the inwards component required using mv^2/r
        totalNeeded = self.mass * abs(self.velocity) ** 2 / abs(fromCentre)

        return totalNeeded - weightInwards
        
class Racetrack(PhysicalObject):
    '''
    Draws a racetrack for the cars on racetracks simulation.
    '''
    
    def __init__(self, radiusP, trackWidth, centre, scaling):
        self.trackWidth = trackWidth
        self.centre = centre
        self.scaling = scaling
        self.radiusP = radiusP
        self.updateFromInput()
    
    def updateFromInput(self):
        self.radius = self.radiusP.value
    
    def display(self):
        # Draw black outside circle with diameter 2 * radius + trackWidth 
        fill(black)
        relXEllipse(self.centre.x * self.scaling, self.centre.y * self.scaling, (2 * self.radius + self.trackWidth) * self.scaling, (2 * self.radius + self.trackWidth) * self.scaling)
        
        # Draw white inner circle with diameeter 2 * radius - trackWidth
        fill(white)
        relXEllipse(self.centre.x * self.scaling, self.centre.y * self.scaling, (2 * self.radius - self.trackWidth) * self.scaling, (2 * self.radius - self.trackWidth) * self.scaling)
        
        # Draw white tracks inside the ring
        noFill()
        stroke(white)
        trackNum = 10 # Number of lines drawn on the track
        angle = TWO_PI / trackNum # Divide the full angle into equal segments
        for i in range(trackNum):
            relXArc(self.centre.x * self.scaling, self.centre.y * self.scaling, 2 * self.radius * self.scaling, 2 * self.radius * self.scaling, i * angle, i * angle + angle / 2.0)
    
class Car(PhysicalObject):
    
    def __init__(self, centre, speedP, radiusP, massP, angleP, muP, relWidth, relHeight, fillColour, scaling):
        self.centre = centre
        self.radiusP = radiusP
        self.speedP = speedP
        self.massP = massP
        self.muP = muP
        self.verticalAngleP = angleP
        self.angleRoundRacetrack = 0
        self.scaling = scaling
        
        self.relWidth = relWidth
        self.relHeight = relHeight
        
        self.fillColour = fillColour
        
        # Initially, the car is still on the race track and not slipping
        self.slipped = 0 # Total amount slipped
        self.slipping = 0 # Direction of slipping
        
        self.updateFromInput()
    
    def update(self, time):
        self.updateFromInput()
        
        # Check forces and update for slipping
        # Solves equations simulationeously:
        # Rcos angle = mg - F sin angle
        # Rsin angle  - F cos angle = m v^2/r
        # R = normal reaction, F = friction UP slope
        c = cos(radians(self.verticalAngle))
        s = sin(radians(self.verticalAngle))
        weight = self.mass * g
        forceNeeded = self.mass * self.speed ** 2 / self.distance
        reaction = weight * c + forceNeeded * s
        friction = weight * s - forceNeeded * c
        
        if friction > reaction * self.mu:
            # Required friction is too large, so it falls down the slope.
            self.slipping = -3
        elif friction < - reaction * self.mu:
            # Required friction is too small, so it slides up the slope.
            self.slipping = 3        
        
        # Update omega and amount slipped
        omega = self.speed / self.distance # Calculate radial acceleration.
        self.angleRoundRacetrack = (self.angleRoundRacetrack + omega * time) % TWO_PI  
        self.slipped += self.slipping * time 
        
        self.updateToOutput()     
    
    def updateFromInput(self):
        # Update all the relevant parameters from the parameters
        self.distance = self.radiusP.value + self.slipped
        self.speed = self.speedP.value
        self.mass = self.massP.value
        self.verticalAngle = self.verticalAngleP.value 
        self.mu = self.muP.value
    
    def initialise(self):
        self.angleRoundRacetrack = 0
        self.slipping = 0
        self.slipped = 0
    
    def display(self):
        noStroke()
        fill(self.fillColour)
        # Rotate the whole coordinates by this angle
        relXRotateAbout(self.centre.x * self.scaling, self.centre.y * self.scaling, self.angleRoundRacetrack)
        # Always draw the rectangle at the bottom
        relXRect((self.centre.x - 0.5 * self.relWidth) * self.scaling, (self.centre.y + self.distance - 0.5 * self.relHeight) * self.scaling, self.relWidth * self.scaling, self.relHeight * self.scaling, 5)
        # Then rotate back, so everything else is drawn correctly
        relXRotateAbout(self.centre.x * self.scaling, self.centre.y * self.scaling, - self.angleRoundRacetrack)

class BreakDownMessage(PhysicalObject):
    def __init__(self, displayText, relX, relY, relWidth, relHeight, fontSize, textColour = color(255, 0, 0)):
        self.displayText = displayText
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        self.fontSize = fontSize
        self.textColour = textColour
        
    def display(self):
        fill(self.textColour)
        textSize(self.fontSize)
        relXText(self.displayText, self.relX, self.relY, self.relWidth, self.relHeight)
        
    def initialise(self):
        self.displayText = "" # Assume no error