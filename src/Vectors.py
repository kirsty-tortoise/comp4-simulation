# TODO:
#    Implement drawAt

class Vector(object):
    
    '''
    A simple class to represent vectors and allow basic vector operations.
    '''

    def __init__(self, x, y):
        # Set up the two components
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        # Vectors are equal iff both components are equal
        return self.x == other.x and self.y == other.y
    
    def __abs__(self):
        # Find the modulus of the vector using trigonometry
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def __add__(self, other):
        # Vectors add component-wise
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        # Vectors subtract component-wise
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        # Implements multiplying vectors by floats
        return Vector(other * self.x, other * self.y)
    
    def __div__(self, other):
        # Implements dividing vectors by floats
        return Vector(self.x / other, self.y / other)
    
    def __rmul__(self, other):
        # Multiplying is the same either way, eg Vector *  5 is 5 * Vector
        return self.__mul__(other)
    
    # The following methods implement augmented assignment (eg a += 1)
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __isub__(self, other):
        return self.__sub__(other)
    
    def __imul__(self, other):
        return self.__mul__(other)
    
    def __idiv__(self, other):
        return self.__div__(other)
    
    def __str__(self):
        # Displays vectors as (x, y) for testing
        return str((self.x, self.y))
    
    def scaleAbs(self, number):
        if self.x == 0 and self.y == 0:
            return Vector(0, 0)
        else:
            return self * number / abs(self)