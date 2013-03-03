'''
Created on 03-03-2013

@author: Marcin
'''

class Graphics:
    '''
    Defines basic interface for all objects returned by Canvas and Predefines
    methods.
    '''
    def mirror(self):
        '''
        reverses the content along the X axis
        '''
        pass

class TextGraphics:
    '''
    Defines basic interface for the object returned from {@link Canvas#text}.
    '''
    def alignStart(self):
        '''
        The position at which this object was created should point to the start
        of the contents.
        '''
        pass
    def alignMiddle(self):
        '''
        The position at which this object was created should point to the middle
        of the contents. This is the default setting.
        '''
        pass
    def alignEnd(self):
        '''
        The position at which this object was created should point to the end
        of the contents.
        '''
        pass

class PolyGraphics:
    '''
    Defines basic interface for the object returned from {@link Canvas#poly}
    and {@link Predefines:poly}.
    '''
    def lineTo(self, x, y):
        '''
        Introduces the next point in the polyline.
        @param x: the x position of the point
        @param y: the y position of the point
        @return: self
        '''
        return None

class Canvas:
    '''
    Provides basic graphics operations. All the coordinates given in its
    methods will be interpreted as offset to the Canvas own origin.
    '''
    def canvas(self, offX, offY, clazz = None):
        '''
        Creates a sub-canvas with an origin offset from current canvas by (offX, offY)
        
        @param offX: the X offset of the new canvas' origin
        @param offY: the Y offset of the new canvas' origin
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def rectangle(self, x, y, width, height, clazz = None):
        '''
        Creates a rectangle at given position with given width and height
        
        @param x: the x position of the rectangle
        @param y: the y position of the rectangle
        @param width: the width of the rectangle
        @param height: the height of the rectangle
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def line(self, x, y, width, height, clazz = None):
        '''
        Creates a line defined as diagonal of a rectangle at given position
        with given width and height. Both width and height can be negative
        and can be zeros.
        
        @param x: the x position of the start of the line
        @param y: the y position of the start of the line
        @param width: the x offset from the start of the line
        @param height: the y offset from the start of the line
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def poly(self, startX, startY, clazz = None):
        '''
        Creates a polyline starting at the given position. Next points can be
        inserted with {@link PolyGraphics#lineTo}
         
        @param startX: the x position of the start of the first line
        @param startY: the y position of the start of the first line
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics and PolyGraphics interfaces
        '''
        return None
    def ref(self, x, y, name, clazz = None):
        '''
        Creates a reference to the object named <code>name</code> and places
        this object at the given coordinates. The referenced object should be
        placed in this printer predefined objects prior to generating the output.
        
        @param x: the x position of referenced object
        @param y: the y position of referenced object
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def text(self, x, y, contents, clazz = None):
        '''
        Creates a text object with the given content and places it
        at the given position. The relation between the text and its postion
        can be defined by TextGraphics methods.
        
        @param x: the x position of the text
        @param y: the y position of the text
        @param contents: the contents of the text object
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics and TextGraphics interfaces
        '''
        return None

class Predefines:
    '''
    Pre-declares objects to be later reffered to by name.
    '''
    def canvas(self, name, offX, offY, clazz = None):
        '''
        Creates a sub-canvas offset from current canvas by (offX, offY), that can later be referenced
        
        @param name: the name of this reference
        @param offX: the X offset of the new canvas
        @param offY: the Y offset of the new canvas
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def rectangle(self, name, x, y, width, height, clazz = None):
        '''
        Creates a rectangle that can later be referenced
        
        @param name: the name of this reference
        @param x: the x position of the rectangle
        @param y: the y position of the rectangle
        @param width: the width of the rectangle
        @param height: the height of the rectangle
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def line(self, name, x, y, width, height, clazz = None):
        '''
        Creates a line that can later be referenced
        
        @param name: the name of this reference
        @param x: the x position of the start of the line
        @param y: the y position of the start of the line
        @param width: the x offset from the start of the line
        @param height: the y offset from the start of the line
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics interface
        '''
        return None
    def poly(self, name, startX, startY, clazz = None):
        '''
        Creates a polyline that can later be referenced
        
        @param name: the name of this reference
        @param startX: the x position of the start of the first line
        @param startY: the y position of the start of the first line
        @param clazz: optional class declaring the look of this entity
        @return: a new object implementing Graphics and PolyGraphics interfaces
        '''
        return None

class Printer:
    '''
    Printer defines a single image.
    '''
    def defs(self):
        '''
        Allows to add predefined objects to the image.
        
        @return: an instance of Predefines
        '''
        return None
    def createCanvas(self, margin, width, height):
        '''
        Creates basic canvas and defines the size of the image contents. The size
        of the resulting image will be <code>width + 2 * margin</code> by
        <code>height + 2 * margin</code>.
        
        @param margin: the margin applied to the image
        @param width: the width of the contents
        @param height: the height of the contents
        @return: an instance of Canvas with origin set to the beginning of the contents
        '''
        return None
    def output(self, out):
        '''
        Writes the contents of the image to the output.
        
        @param out: The output for the image; a file of file-like object. The only method used is <code>write(str)</code>
        '''
        pass
