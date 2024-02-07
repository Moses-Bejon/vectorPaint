from tkinter import *
from VectorPaintController import VectorPaintController
from VectorPaintModel import VectorPaintModel
from VectorPaintView import *

root = Tk()
root.title("Vector paint project")

model = VectorPaintModel()
controller = VectorPaintController(model)

canvas = myCanvas(root, controller,model) # called it mycanvas because canvas already exists :(
tree = treeView(root, controller,model) # Shows the clickable buttons for moving around the tree
buttonBar = canvas.buttonBar # the canvas is composed of the button bar, so I want to grid the canvas's button bar
menuBar = MenuBar(root,controller) # save, save as and load

menuBar.frame.grid(column=0,row=0,columnspan=3,sticky="E")
canvas.frame.grid(column=2,row=1,sticky=NSEW)
tree.frame.grid(column=0,row=1,sticky=N)
buttonBar.grid(column=1,row=1,sticky=N)
root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(2,weight=1)

root.mainloop()
