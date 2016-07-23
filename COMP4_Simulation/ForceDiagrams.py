# TODO:

from RelativeDrawing import relXImage

class ForceDiagram(object):
    def __init__(self, name, imageFileName, relX = 0.5, relY = 0.03, relWidth = 0.5, relHeight = 0.32):
        self.name = name
        self.diagramImage = loadImage(imageFileName)
        self.relX = relX
        self.relY = relY
        self.relWidth = relWidth
        self.relHeight = relHeight
        
    def display(self):
        relXImage(self.diagramImage, self.relX, self.relY, self.relWidth, self.relHeight)
    
    def update(self):
        pass # No updating required.