from tkinter import *

from canvasElements import *

from sys import platform
if platform == "darwin":
    from tkmacosx import Button

class ButtonBar:
    def __init__(self, root_frame,controls, width):

        self.__root_frame = root_frame
        self.__controls = controls

        self.frame = Frame(self.__root_frame, width=width)

        self.__buttons = [[Label(self.frame,text="fill colour"), Button(self.frame, text="Red", command=lambda: self.__controls.set_colour("Red")), Button(self.frame, text="Black", command=lambda: self.__controls.set_colour("Black")),Button(self.frame, text="Blue", command=lambda: self.__controls.set_colour("Blue")),Button(self.frame, text="White", command=lambda: self.__controls.set_colour("White"))],
                          [Label(self.frame,text="outline colour"), Button(self.frame, text="Red", command=lambda: self.__controls.set_outline_colour("Red")), Button(self.frame, text="Black", command=lambda: self.__controls.set_outline_colour("Black")),Button(self.frame, text="Blue", command=lambda: self.__controls.set_outline_colour("Blue")),Button(self.frame, text="White", command=lambda: self.__controls.set_outline_colour("White"))],
                          [Label(self.frame, text="back ground colour"),Button(self.frame, text="Red", command=lambda: self.__controls.set_background_colour("Red")),Button(self.frame, text="Black",command=lambda: self.__controls.set_background_colour("Black")),Button(self.frame, text="Blue", command=lambda: self.__controls.set_background_colour("Blue")),Button(self.frame, text="White",command=lambda: self.__controls.set_background_colour("White"))],
                          [Label(self.frame,text="shape"), Button(self.frame, text="Line", command=lambda: self.__controls.set_shape(Line)),Button(self.frame, text="Rectangle", command=lambda: self.__controls.set_shape(Rectangle))]]

        width = len(self.__buttons[0])
        height = len(self.__buttons)

        for column,buttons in enumerate(self.__buttons):
            for row,button in enumerate(buttons):
                button.grid(row=row,column=column)
            self.frame.columnconfigure(column)
        for row in range(width):
            self.frame.rowconfigure(row)

        self.__borderScaler = Scale(self.frame,orient=HORIZONTAL,command=controls.set_outline_thickness)

        Label(self.frame,text="shape border size:").grid(row=height+1,column=0)
        self.__borderScaler.grid(row=height+1,column=1,columnspan=width-1,sticky="NSEW")

class myCanvas:
    def __init__(self, root_frame):
        self.__root_frame = root_frame

        self.__currColour = "Red"
        self.__currOutlineColour = "Red"
        self.__currOutlineThickness = 0
        self.__currShape = Line
        self.__currPlace = None

        self.frame = Canvas(self.__root_frame, bg = "White")

        self.frame.bind("<Button-1>", self.start_draw)
        self.frame.bind("<ButtonRelease-1>", self.stop_draw)
        self.frame.bind("<B1-Motion>", self.continue_draw)

    def set_colour(self, colour):
        self.__currColour = colour

    def set_outline_colour(self,colour):
        self.__currOutlineColour = colour

    def set_outline_thickness(self,thickness):
        self.__currOutlineThickness = thickness

    def set_background_colour(self,colour):
        self.frame.config(bg=colour)

    def set_shape(self, shape):
        self.__currShape = shape

    def start_draw(self, event):
        self.__currObject = self.__currShape(self.frame,event,self.__currColour,self.__currOutlineColour,self.__currOutlineThickness)

    def continue_draw(self, event):
        self.__currObject.continue_draw(event)

    def stop_draw(self, event):
        self.continue_draw(event)
        self.__currObject = None
