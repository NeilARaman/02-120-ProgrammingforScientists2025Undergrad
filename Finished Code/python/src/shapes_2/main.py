# five fields for rectangle:
# width, height, x1, y1 (center or top left), rotation

# place class declarations between imports and def main

class Rectangle:
    """
    Represents a 2D rectangle with width, height, position, and rotation

    Attributes:
        width: (float)
        height: (float)
        x1: the x-coordinate of the rectangle's origin (float)
        y1: the y-coordinate of the rectangle's origin (float)
        rotation: rotation of shape in degrees (float)
    
    Class Attributes:
        description: describes some characteristic of the object (string) 
    """

    description: str = "boxy"

    # Every class declaration should have a constructor to set fields
    # Also, Python calls fields "attributes"
    # We will allow the user to set attributes of an instance the second it is born
    def __init__(self, width: float=0.0, height: float=0.0, x1: float=0.0, y1: float=0.0, rotation: float=0.0):
        # let's protect the program from a bad user 
        if width < 0.0 or height < 0.0:
            raise ValueError("width and height must be nonnegative.")
        # we could add tests for if variables are all floats, etc.
        
        # what attributes should every Rectangle get?
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.rotation = rotation

    def __repr__(self) -> str:
        # let's have a nice f string to print the attributes 
        return f"Rectangle(width={self.width},height={self.height},x1={self.x1}, y1={self.y1}, rotation={self.rotation})"
    
    def area(self) -> float:
        """Method to return the area of rectangle."""
        return self.width * self.height
    
    def translate(self, a: float, b: float) -> None:
        """Method to translate a shape a units in the x direction and b units in the y direction"""
        self.x1 += a 
        self.y1 += b

    def scale(self, f: float):
        """Dilate the shape by a factor of f."""
        self.width *= f
        self.height *= f


class Circle:
    """
    Represents a 2D circle via its center and radius.
    
    Attributes:
        x1: the x-coordinate of the center (float)
        y1: the y-coordinate of the center (float)
        radius: the center's radius (float)

    Class Attributes:
        description: describes some characteristic of the object (string) 
    """

    description: str = "round"

    def __init__(self, x1: float=0, y1: float = 0, radius: float = 0):
        if radius < 0.0:
            raise ValueError("width and height must be nonnegative.")
        self.x1 = x1
        self.y1 = y1
        self.radius = radius

    def __repr__(self) -> str:
        # let's have a nice f string to print the attributes 
        return f"Circle(x1={self.x1}, y1={self.y1}, radius={self.radius})"
    
    def area(self) -> float:
        """Method to compute area of circle."""
        return 3.0 * self.radius ** 2
    
    def translate(self, a: float, b: float) -> None:
        """Method to translate a shape a units in the x direction and b units in the y direction"""
        self.x1 += a 
        self.y1 += b

    def scale(self, f: float):
        """Dilate the shape by a factor of f."""
        self.radius *= f    

# Mutable things are pass by reference
# Lists
# Dictionaries
# User-defined classes (rectangles, bodies, trees, etc.)

# Immutable things are pass by value 
# tuples 
# strings 
# ints, floats, booleans

# there is one explanation for all of this: in Python, everything is an object, and everything is "pass by object reference"

def main():
    print("Shapes part 2.")

    # basic_shape_stuff()

    # list_stuff()

    # when you make a variable, python gives it a numeric ID (like an Andrew ID)
    # we access it with the id() function

    n = 5 
    print("Outside function before change:", n, id(n))

    change_value(n)

    print("Outside function after change:", n, id(n))

    # id() is useful because if we have two objects we can check if they are actually the same literal object

    r1 = Rectangle(width = 3.0, height = 4.0, x1 = 0.0, y1 = 0.0)
    print("Original r1:", r1)

    # new question: what happens if ......
    r2 = r1

    # we copied over the attributes! yay

    print("r2 is:", r2)

    # not really. What we did was say, r2 has the same object reference as r1

    # I can prove it 
    if id(r1) == id(r2):
        print("We have two references to the same rectangle.")

    r2.translate(10, 5)
    
    print("After translating ...")
    print("r1 is:", r1)
    print("r2 is:", r2)

    # if I want to make a copy of the rectangle, what should I do?
    # idea 1: make a function (better)
    # idea 2: use init with the fields of the first thing 

    r3 = Rectangle(width = r1.width, height = r1.height, x1 = r1.x1, y1 = r1.y1, rotation = r1.rotation)







def change_value(x:int) -> None:
    print("Inside function before change:", x, id(x))

    # presumably, the id(x) should not be id(n). A copy got created because it's pass by value. Right?

    # but it's not. When you pass even an integer into the function, you are passing the literal integer in by (object) reference

    x += 10 # when this happens, a new variable with name x gets created

    print("Inside function after change:", x, id(x))


def list_stuff():
    a = [0] * 10
    change_first(a)
    print(a)

    # this happens not because lists are pass by reference (that is true) but because lists are mutable, and mutable things are pass by reference

    # set values for a 
    for i in range(len(a)):
        a[i] = -i-1

    q = a[8:10] # q makes a copy of the data in a 
    # note: another instance of python slowness
    
    print("a is", a)
    print("q is", q)

    # let's change an element of a
    a[9] = 666

    # does q also change? In some languages, it does, and it others, it doesn't

    print("a is", a)
    print("q is", q)

    # it does not change q

def change_first(lst: list[int]) -> None:
    lst[0] = 1

def basic_shape_stuff():  

    # let's make some shapes 
    r = Rectangle(height = 4.0, width = 3.0) # we don't even need to get the parameter order right in init if we specify their attributes

    c = Circle(x1 = 0.0, y1=0.0, radius=4.0)

    print(r)
    print(c)

    # now let's print the areas of the rectangles
    print("Rectangle area:", r.area())
    print("Circle area:", c.area())

    # when we see math.sqrt() or random.randrange(0,3) or pygame.draw.circle(), it's not quite this. It means go into the math module and grab the sqrt() function

    # we've used methods a lot!
    # dict.keys(), or dict.values()
    # .split(), .strip(), etc. in I/O: list methods
    # lst.append(item) -- built in method of lists
    # drawing: surface.fill(dark_gray)

    # The reason why something basic like a list has a method is that in Python, EVERYTHING is an object (this is part of why it is so slow and painful)

    # we have our shapes, so let's translate them 
    r.translate(10.0, -5.0)
    c.translate(2.5, 3.5)

    print("After translation:")
    print(r)
    print(c)

    # as we might hope, the shapes move, because we passed r and c as inputs to translate, and in Python, user-defined classes are pass by reference 

    # scale both shapes 
    r.scale(2.0)
    c.scale(0.4)
    print("After scaling:")
    print(r)
    print(c)

    # Note: areas scale by a factor of f^2
    print("New rectangle area:", r.area())
    print("New circle area:", c.area())

def area_rectangle(r: Rectangle) -> float:
    """
    Compute the area of a given rectangle.
    """
    return r.width * r.height

def area_circle(c: Circle) -> float:
    """
    Compute the area of a circle.
    """
    return 3.0 * (c.radius ** 2)

# write perimeter_rectangle() and perimeter_circle() functions

def translate_rectangle(r: Rectangle, a: float, b:float) -> None:
    """
    Move a rectangle by a given amount in x- and y-directions.
    """
    r.x1 += a 
    r.y1 += b 

def translate_circle(c: Circle, a: float, b:float) -> None:
    """
    Move a circle by a given amount in x- and y-directions.
    """
    c.x1 += a
    c.y1 += b

if __name__ == "__main__":
    main()