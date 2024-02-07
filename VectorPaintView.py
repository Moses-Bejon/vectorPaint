from tkinter import *

from canvasElements import *

from sys import platform
if platform == "darwin":
    from tkmacosx import Button

class MenuBar():
    def __init__(self, root_frame,controller):
        self.__root_frame = root_frame
        self.__controller = controller

        self.frame = Frame(self.__root_frame)

        self.__buttons = [Button(self.frame,text="Save As",command=controller.saveAs),Button(self.frame,text="Save",command=controller.save),Button(self.frame,text="Load",command=controller.load)]
        for button in self.__buttons:
            button.pack(side=LEFT)

class myCanvas:
    def __init__(self, root_frame, controller, model):
        self.__root_frame = root_frame
        self.__controller = controller

        # button bar stuff

        self.buttonBar = Frame(self.__root_frame)

        # This only happens to be in neat short lines because the buttons are arranged in the array the same way they
        # are in the view. This is a coincidence.
        self.__buttons = [
            Button(self.buttonBar, text="Draw", command=lambda: self.set_shape(Drawing), width=70, height=70),
            Button(self.buttonBar, text="Line", command=lambda: self.set_shape(Line), width=70, height=70),
            Button(self.buttonBar, text="Rectangle", command=lambda: self.set_shape(Rectangle), width=70, height=70),
            Button(self.buttonBar, text="Oval", command=lambda: self.set_shape(Oval), width=70, height=70)]

        for i, button in enumerate(self.__buttons):
            button.grid(column=1, row=i)

        height1 = len(self.__buttons)

        self.__borderScaler = Scale(self.buttonBar, orient=VERTICAL, command=self.set_outline_thickness, showvalue=0,
                                    from_=100, to=0)
        self.__borderScaler.grid(column=0, row=0, rowspan=height1, sticky=NSEW)

        # tkinter thing - allows me to know when the values in the entries change - yeah, I don't like tkinter either
        self.__fillSet = StringVar(value="#FFFFFF")
        self.__outlineSet = StringVar(value="#808080")
        self.__backgroundSet = StringVar(value="#000000")

        # another coincidence
        self.__colours = [[Label(self.buttonBar, text="back-ground\n colour:"),
                           Entry(self.buttonBar, width=7,textvariable=self.__backgroundSet)],
                          [Label(self.buttonBar, text="fill colour:"),
                           Entry(self.buttonBar, width=7,textvariable=self.__fillSet)],
                          [Label(self.buttonBar, text="outline colour:"),
                           Entry(self.buttonBar, width=7,textvariable=self.__outlineSet)]]

        for i, pair in enumerate(self.__colours):
            pair[0].grid(column=0, row=height1 + 2 * i, columnspan=2)
            pair[1].grid(column=0, row=height1 + 2 * i + 1, columnspan=2)

        # canvas stuff

        self.frame = Canvas(self.__root_frame)

        self.set_colour("#FFFFFF")
        self.set_outline_colour("#808080")
        self.set_background_colour("#000000")

        # This allows me to run the function when the entry values change. Any reasonable GUI library would have it
        # so the entries trigger an event and pass the value they changed to but no, I had to set up new variables
        # that cluttered up my code just so I could implement this basic functionality.
        self.__fillSet.trace("w", self.changeColour)
        self.__backgroundSet.trace("w", self.changeBackgroundColour)
        self.__outlineSet.trace("w", self.changeOutlineColour)

        self.__currOutlineThickness = 0
        self.__currShape = Drawing
        self.__currPlace = None

        model.subscribe(self)

        self.frame.bind("<Button-1>", self.start_draw)
        self.frame.bind("<ButtonRelease-1>", self.stop_draw)
        self.frame.bind("<B1-Motion>", self.continue_draw)

    # tkinter passes in three values when it changes and none of them are the value it changes to...
    def changeColour(self,nonsense=None,rubbish=None,gibberish=None):
        colour = self.__fillSet.get()
        try:
            if encodeColour(colour)[0] > 200 and encodeColour(colour)[1] > 200 and encodeColour(colour)[2] > 200:
                self.__colours[1][0].config(fg="#000000")
            else:
                self.__colours[1][0].config(fg="#FFFFFF")
            self.__colours[1][0].config(bg=colour)
            self.__currColour = colour
        except:
            pass

    def set_colour(self, colour):
        self.__fillSet.set(colour)
        self.changeColour()

    def set_outline_colour(self,colour):
        self.__backgroundSet.set(colour)
        self.changeOutlineColour()

    def changeOutlineColour(self,nonsense=None,rubbish=None,gibberish=None):
        colour = self.__outlineSet.get()
        try:
            if encodeColour(colour)[0] > 200 and encodeColour(colour)[1] > 200 and encodeColour(colour)[2] > 200:
                self.__colours[2][0].config(fg="#000000")
            else:
                self.__colours[2][0].config(fg="#FFFFFF")
            self.__colours[2][0].config(bg=colour)
            self.__currOutlineColour = colour
        except:
            pass
    def set_outline_thickness(self,thickness):
        self.__currOutlineThickness = thickness

    def set_background_colour(self,colour):
        self.__backgroundSet.set(colour)
        self.changeBackgroundColour()

    def changeBackgroundColour(self,nonsense=None,rubbish=None,gibberish=None):
        colour = self.__backgroundSet.get()
        try:
            if encodeColour(colour)[0] > 200 and encodeColour(colour)[1] > 200 and encodeColour(colour)[2] > 200:
                self.__colours[0][0].config(fg="#000000")
            else:
                self.__colours[0][0].config(fg="#FFFFFF")
            self.__colours[0][0].config(bg=colour)
            self.frame.config(bg=colour)
        except:
            pass

    def set_shape(self, shape):
        self.__currShape = shape

    def saveState(self):
        # saving my colour
        return encodeColour(self.frame.cget("bg"))

    def setState(self,bytes):
        bytes, colour = decodeColour(bytes)
        self.set_background_colour(colour)

        return bytes

    def clear(self):
        self.frame.delete("all")

    def start_draw(self, event):
        self.__currObject = self.__currShape()
        self.__currObject.canvasSet(self.frame,int(event.x),int(event.y),self.__currColour,self.__currOutlineColour,self.__currOutlineThickness)

    def continue_draw(self, event):
        self.__currObject.canvasUpdate(int(event.x), int(event.y))

    def stop_draw(self, event):
        self.__controller.add(self.__currObject)
        self.__currObject = None

    def add(self,item):
        # already added it bucko
        pass

    def loadItem(self,item):
        # lettin' 'em know who I am
        item.giveRoot(self.frame)

    def goTo(self,previous,new):
        # all items in route need to be shown on the canvas and are currently not shown
        route = []

        difference = previous.getLayer()-new.getLayer()

        # ensures items are on the same layer
        if difference > 0:
            for _ in range(difference):
                previous.hide()
                previous = previous.getParent()
        else:
            for _ in range(-difference):
                route.append(new)
                new = new.getParent()

        # Go up the tree until reach common ancestor
        while new != previous:
            route.append(new)
            new = new.getParent()
            previous.hide()
            previous = previous.getParent()

        # show all items in correct order
        for item in route[::-1]:
            item.show()


class treeView:
    def __init__(self,root_frame,controller, model):
        self.__root_frame = root_frame
        self.__controller = controller

        self.__layers = []
        self.frame = Frame(self.__root_frame)

        model.subscribe(self)

    def saveState(self):
        # I'm a simple guy, don't need to save anything
        return []

    def setState(self,bytes):
        # and so I don't decode anything either
        return bytes

    def clear(self):
        for layer in self.__layers:
            for button in layer:
                button.destroy()
        self.__layers = []

    def add(self, item):

        # if the layer doesn't exist, make it, otherwise add it on to the existing layer
        if item.getLayer() >= len(self.__layers):
            self.__layers.append([Button(self.frame,text=item.getName()+" ID: "+str(item.getID()),command=lambda: self.__controller.goTo(item),width=100)])
        else:
            self.__layers[item.getLayer()].append(Button(self.frame,text=item.getName()+" ID: "+str(item.getID()),command=lambda: self.__controller.goTo(item),width=100))

        self.update()

    def loadItem(self, item):
        self.add(item)

    def goTo(self,previous,new):
        pass

    def update(self):
        for row,layer in enumerate(self.__layers):
            for column,item in enumerate(layer):
                item.grid(row=row,column=column)
            self.frame.grid_rowconfigure(row, weight=1)
        for i in max(self.__layers,key=lambda x:len(x)):
            self.frame.grid_columnconfigure(i,weight=1)









