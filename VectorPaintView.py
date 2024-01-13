from tkinter import *

from canvasElements import *

from sys import platform
if platform == "darwin":
    from tkmacosx import Button

class ButtonBar:
    def __init__(self, root_frame,controls, width):

        self.__root_frame = root_frame
        self.__controls = controls

        self.frame = Frame(self.__root_frame, bg="Gray", width=width)

        self.__buttons = [[Button(self.frame, text="Black", command=lambda: self.__controls.set_colour("Black")),Button(self.frame, text="Blue", command=lambda: self.__controls.set_colour("Blue"))],[Button(self.frame, text="Line", command=lambda: self.__controls.set_shape(Line)),Button(self.frame, text="Rectangle", command=lambda: self.__controls.set_shape(Rectangle))]]
        for column,buttons in enumerate(self.__buttons):
            for row,button in enumerate(buttons):
                button.grid(row=row,column=column)
            self.frame.columnconfigure(column)
        for row in range(len(self.__buttons[0])):
            self.frame.rowconfigure(row)

class myCanvas:
    def __init__(self, root_frame):
        self.__root_frame = root_frame

        self.__currColour = "Red"
        self.__currShape = Line
        self.__currPlace = None

        self.frame = Canvas(self.__root_frame, bg = "White")

        self.frame.bind("<Button-1>", self.start_draw)
        self.frame.bind("<ButtonRelease-1>", self.stop_draw)
        self.frame.bind("<B1-Motion>", self.continue_draw)

        self.resize()

    def resize(self):
        pass

    def set_colour(self, colour):
        self.__currColour = colour

    def set_shape(self, shape):
        self.__currShape = shape

    def start_draw(self, event):
        self.__currObject = self.__currShape(self.frame,event,self.__currColour)

    def continue_draw(self, event):
        self.__currObject.continue_draw(event)

    def stop_draw(self, event):
        self.continue_draw(event)
        self.__currObject = None
