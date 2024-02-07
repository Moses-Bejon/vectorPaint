from tkinter import filedialog

class VectorPaintController:
    def __init__(self,model):
        self.__model = model
        self.__fileName = None

    # you may think I'm just a telephone...
    def add(self,item):
        self.__model.add(item)

    # I did too at one point in my life...
    def goTo(self,item):
        self.__model.goTo(item)

    # BUT IM NOT!!!!
    def saveAs(self):

        fileName = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                 title="Save As"
                                                )

        self.__model.saveAs(fileName)
        self.__fileName = fileName

    # I HAVE LOGIC!!!!!!!!
    def save(self):
        if self.__fileName:
            self.__model.saveAs(self.__fileName)

    # LOOK AT ME MUM I DID IT!!!!!!!!!!!!!!!!!!
    def load(self):
        fileName = filedialog.askopenfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                 title="Save As")
        self.__model.load(fileName)
        self.__fileName = fileName