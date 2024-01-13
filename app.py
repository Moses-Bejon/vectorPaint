from tkinter import *
import VectorPaintView



root = Tk()

canvas = VectorPaintView.myCanvas(root)
buttonBar = VectorPaintView.ButtonBar(root,canvas,50)
canvas.set_scaler(buttonBar.getBorderScale)

canvas.frame.pack(side=RIGHT, fill=BOTH, expand=True)
buttonBar.frame.pack(side=LEFT, fill=Y)

root.mainloop()
