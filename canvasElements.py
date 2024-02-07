from tkinter import *

# this file contains some commonly used functions and classes

# first byte is the length of the rest of the encoded integer.
# Next bytes are written with the least significant byte on the left
def encode(value):
    if value > 0:
        place = 1
        values = [0]
        while value != 0:
            values.append(value % 256)
            value = value // 256
            place += 1

        values[0] = (place - 1)
        return values
    else:
        return [0]

# returns the rest of the file and the number it decoded
def decode(bytes):
    digits = bytes.pop(0)
    number = 0
    for place,digit in enumerate(bytes[0:digits]):
        number = number + digit*(256**place)
        bytes.pop(0)
    return (bytes,number)

def encodeColour(colour):
    values = []
    for hex in colour[1:]:
        if ord(hex) >= 65:
            values.append(ord(hex)-55)
        else:
            values.append(int(hex))
    return [values[0]*16+values[1],values[2]*16+values[3],values[4]*16+values[5]]

def decodeColour(bytes):
    colour = "#"
    for byte in bytes[:3]:

        if byte//16 >= 10:
            colour += chr(byte//16+55)
        else:
            colour += str(byte//16)

        if byte%16 >= 10:
            colour += chr(byte%16+55)
        else:
            colour += str(byte%16)

        bytes.pop(0)

    return (bytes,colour)

# recursive algorithm that encodes all the items in the tree
def save(rootNode):
    output = []

    for child in rootNode.getChildren():
        output += child.encode()
        output += save(child)
    return output

class Root():
    def __init__(self):
        self.__children = []

    def addChild(self,child):
        self.__children.append(child)

    def getParent(self):
        return None # the very first chicken

    def getChildren(self):
        return self.__children

    def getLayer(self):
        return 0

    def giveRoot(self,nonsense):
        pass # this is how you give an object its root frame, but the Root has no root frame because it is not a shape

    def getName(self):
        return "reset" # tree displays this as reset as when you click it it resets

    def hide(self):
        pass

    def show(self):
        pass

    def treeSet(self,nonsense,rubbish):
        pass # the root doesn't have a parent and it knows its ID from birth

    def getID(self):
        return 0

# abstract class for all shapes
class Shape():
    def __init__(self):
        self.__children = []
        self._coords_list = []

    def canvasUpdate(self, x, y):
        if x > self._place[0]:
            self._coords_list[0] = self._place[0]
            self._coords_list[2] = x
        else:
            self._coords_list[2] = self._place[0]
            self._coords_list[0] = x
        if y > self._place[1]:
            self._coords_list[1] = self._place[1]
            self._coords_list[3] = y
        else:
            self._coords_list[3] = self._place[1]
            self._coords_list[1] = y
        self.draw()

    def draw(self):
        self._root_frame.coords(self._geometry, self._coords_list)

    def hide(self):
        self._root_frame.delete(self._geometry)

    def addChild(self, child):
        self.__children.append(child)

    def encode(self):
        return [self._identity]+encode(self.__parent.getID()) + encode(self.__ID) + encodeColour(self._colour) + [self._size]

    def decode(self,bytes):
        bytes,self.__ID = decode(bytes)
        bytes,self._colour = decodeColour(bytes)
        self._size = bytes.pop(0)

        return bytes

    def setData(self, place):
        self._place = place
        self._coords_list = [place[0], place[1], place[0], place[1]]

    def giveRoot(self,root):
        self._root_frame = root

    def treeSet(self,parent,ID):
        self.__ID = ID
        self.__parent = parent
        self.__layer = parent.getLayer()+1

    def setParent(self,parent):
        self.__parent = parent
        self.__layer = parent.getLayer() + 1

    def canvasSet(self,root_frame, place):
        self._root_frame = root_frame
        self._place = place
        self._coords_list = [place[0], place[1], place[0], place[1]]

    def getParent(self):
        return self.__parent

    def getChildren(self):
        return self.__children

    def getLayer(self):
        return self.__layer

    def getName(self):
        return self._name

    def getID(self):
        return self.__ID

class Drawing(Shape):
    def __init__(self):
        super().__init__()
        self.__geometries = []
        self.__points = []

        self._name = "drawing"
        self._identity = 0

    def canvasSet(self, root_frame, x,y, colour, outlineColour, outlineScale):
        super().canvasSet(root_frame, (x, y))
        self._colour = colour
        self._size = int(outlineScale)
        self.__points = [(x, y)]

    def setData(self, x,y, colour, outlineColour, outlineScale):
        super().setData((x, y))
        self._colour = colour
        self._size = int(outlineScale)
        self.__points = [(x, y)]

    def canvasUpdate(self, x, y):
        self.__geometries.append(self._root_frame.create_line(self.__points[-1][0], self.__points[-1][1], x, y, fill=self._colour, width=self._size))
        if self._size >= 2:
            self.__geometries.append(self._root_frame.create_oval(x + 0.5 * self._size, y + 0.5 * self._size, x - 0.5 * self._size, y - 0.5 * self._size, fill=self._colour, width=0))
        self.__points.append((x, y), )
    def hide(self):
        for geometry in self.__geometries:
            self._root_frame.delete(geometry)
        self.__geometries = []
    def show(self):
        for i in range(len(self.__points)-1):
            self.__geometries.append(self._root_frame.create_line(self.__points[i][0], self.__points[i][1], self.__points[i+1][0], self.__points[i+1][1], fill=self._colour, width=self._size))
            if self._size >= 2:
                self.__geometries.append(self._root_frame.create_oval(self.__points[i][0] + 0.5 * self._size, self.__points[i][1] + 0.5 * self._size, self.__points[i][0] - 0.5 * self._size, self.__points[i][1] - 0.5 * self._size, fill=self._colour, width=0))

    def encode(self):
        output = super().encode()

        output += encode(len(self.__points))
        # How long is points and how long is the number that stores that number


        for point in self.__points:
            output += encode(point[0])
            output += encode(point[1])

        return output

    def decode(self,bytes):
        bytes = super().decode(bytes)
        bytes, points = decode(bytes)

        for point in range(points):
            bytes,x = decode(bytes)
            bytes,y = decode(bytes)
            self.__points.append((x,y),)

        return bytes

class Line(Shape):
    def __init__(self):
        super().__init__()

        self._name = "line"
        self._identity = 1

    def canvasSet(self, root_frame, x,y, colour, outlineColour, outlineScale):
        super().canvasSet(root_frame,(x,y))
        self._colour = colour
        self._size = int(outlineScale)
        self._geometry = self._root_frame.create_line(x, y, x, y, fill=self._colour, width=self._size)

    def setData(self, x,y, colour, outlineColour, outlineScale):
        super().setData((x,y))
        self._colour = colour
        self._size = int(outlineScale)
        self._geometry = self._root_frame.create_line(x, y, x, y, fill=self._colour, width=self._size)

    def canvasUpdate(self, x, y):
        self._coords_list[2] = x
        self._coords_list[3] = y
        self.draw()

    def show(self):
        self._geometry = self._root_frame.create_line(self._coords_list[0],self._coords_list[1],self._coords_list[2],self._coords_list[3],fill=self._colour,width=self._size)

    def encode(self):
        output = super().encode()
        for coord in self._coords_list:
            output += encode(coord)
        return output
    def decode(self,bytes):
        bytes = super().decode(bytes)
        for _ in range(4):
            bytes, coord = decode(bytes)
            self._coords_list.append(coord)
        return bytes


class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self._name = "rectangle"
        self._identity = 2

    def canvasSet(self, root_frame, x,y, colour, outlineColour, outlineScale):
        super().canvasSet(root_frame,(x,y))
        self._colour = colour
        self.__outlineColour = outlineColour
        self._size = int(outlineScale)
        self._geometry = self._root_frame.create_rectangle(x, y, x, y, fill=self._colour, outline=self.__outlineColour,width=self._size)

    def setData(self, x, y, colour, outlineColour, outlineScale):
        super().setData((x, y))
        self._colour = colour
        self._size = int(outlineScale)
        self.__outlineColour = outlineColour
        self._geometry = self._root_frame.create_rectangle(x, y, x, y, fill=self._colour, outlineColour=self.__outlineColour,width=self._size)

    def show(self):
        self._geometry = self._root_frame.create_rectangle(self._coords_list[0], self._coords_list[1], self._coords_list[2], self._coords_list[3], fill=self._colour,outline=self.__outlineColour, width=self._size)

    def encode(self):
        output = super().encode() + encodeColour(self.__outlineColour)
        for coord in self._coords_list:
            output += encode(coord)
        return output

    def decode(self,bytes):
        bytes = super().decode(bytes)
        bytes, self.__outlineColour = decodeColour(bytes)
        for _ in range(4):
            bytes, coord = decode(bytes)
            self._coords_list.append(coord)
        return bytes



class Oval(Shape):
    def __init__(self):
        super().__init__()

        self._name = "oval"
        self._identity = 3

    def canvasSet(self, root_frame, x,y, colour, outlineColour, outlineScale):
        super().canvasSet(root_frame,(x,y))
        self._colour = colour
        self.__outlineColour = outlineColour
        self._size = int(outlineScale)
        self._geometry = self._root_frame.create_oval(x, y, x, y, fill=self._colour, outline=self.__outlineColour,width=self._size)

    def setData(self, x, y, colour, outlineColour, outlineScale):
        super().setData((x, y))
        self._colour = colour
        self._size = int(outlineScale)
        self.__outlineColour = outlineColour
        self._geometry = self._root_frame.create_oval(x, y, x, y, fill=self._colour, outlineColour=self.__outlineColour,width=self._size)

    def show(self):
        self._geometry = self._root_frame.create_oval(self._coords_list[0], self._coords_list[1], self._coords_list[2], self._coords_list[3], fill=self._colour, outline=self.__outlineColour,width=self._size)

    def encode(self):
        output = super().encode() + encodeColour(self.__outlineColour)
        for coord in self._coords_list:
            output += encode(coord)
        return output

    def decode(self,bytes):
        bytes = super().decode(bytes)
        bytes, self.__outlineColour = decodeColour(bytes)
        for _ in range(4):
            bytes, coord = decode(bytes)
            self._coords_list.append(coord)
        return bytes
