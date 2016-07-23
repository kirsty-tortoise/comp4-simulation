# These functions define the usual drawing functions, but with relative coordinates from 0 to 1.

def relRect(relX, relY, relW, relH, c = 0):
    rect(relX * width, relY * height, relW * width, relH * height, c)

def relEllipse(relX, relY, relW, relH):
    ellipse(relX * width, relY * height, relW * width, relH * height)

def relText(t, relX, relY, relW, relH, relIndent = 0):
    text(t, (relX + relIndent)  * width, relY * height, relW * width, relH * height)

def relTriangle(relX1, relY1, relX2, relY2, relX3, relY3):
    triangle(relX1 * width, relY1 * height, relX2 * width, relY2 * height, relX3 * width, relY3 * height)

def relLine(relX1, relY1, relX2, relY2):
    line(relX1 * width, relY1 * height, relX2 * width, relY2 * height)
    
def relImage(im, relX, relY, relW, relH):
    image(im, relX * width, relY * height, relW * width, relH * height)
    
def relIsOver(relX, relY, relW, relH):
    '''
    Checks if the mouse is over the button described by the relative coordinates
    '''
    return relX * width <= mouseX <= width * (relX + relW) and relY * height <= mouseY <= height * (relY + relH)

# These functions are the same, but only relative to X (changing the height makes no difference)

def relXRect(relX, relY, relW, relH, c = 0):
    rect(relX * width, relY * width, relW * width, relH * width, c)

def relXPoint(relX, relY):
    point(relX * width, relY * width)

def relXEllipse(relX, relY, relW, relH):
    ellipse(relX * width, relY * width, relW * width, relH * width)

def relXText(t, relX, relY, relW = None, relH = None, relIndent = 0):
    if relW is None:
        text(t, (relX + relIndent)  * width, relY * width)
    else:
        text(t, (relX + relIndent)  * width, relY * width, relW * width, relH * width)

def relXTriangle(relX1, relY1, relX2, relY2, relX3, relY3):
    triangle(relX1 * width, relY1 * width, relX2 * width, relY2 * width, relX3 * width, relY3 * width)

def relXLine(relX1, relY1, relX2, relY2):
    line(relX1 * width, relY1 * width, relX2 * width, relY2 * width)
    
def relXImage(im, relX, relY, relW, relH):
    image(im, relX * width, relY * width, relW * width, relH * width)
    
def relXArc(a, b, c, d, start, stop):
    arc(a * width, b * width, c * width, d * width, start, stop)
    
def relXIsOver(relX, relY, relW, relH):
    '''
    Checks if the mouse is over the button described by the relative coordinates
    '''
    return relX * width <= mouseX <= width * (relX + relW) and relY * width <= mouseY <= width * (relY + relH)

def relXRotateAbout(relX, relY, angle):
    '''
    Rotates coordinate system about the point relX, relY. 
    '''
    translate(relX * width, relY * width) # translate to origin
    rotate(angle) 
    translate(- relX * width, - relY * width) # Then translate back
    pass