from canvasElements import *

class VectorPaintModel:
    def __init__(self):
        self.__root = Root()
        self.__currentItem = self.__root

        self.__subscribers = []

        self.__next_item_id = 1

    def clear(self):
        self.__root = Root()
        self.__currentItem = self.__root

        # telling my subscribers about this very sad event... :(
        for subscriber in self.__subscribers:
            subscriber.clear()

        self.loadItem(self.__root)

    def add(self,item):
        self.__currentItem.addChild(item)
        item.treeSet(self.__currentItem,self.__next_item_id)

        # telling my subscribers the good news! :)
        for subscriber in self.__subscribers:
            subscriber.add(item)

        self.__next_item_id += 1
        self.__currentItem = item

    # load is loading from a file, add is when a view tells me to add
    def loadItem(self,item):
        for subscriber in self.__subscribers:
            subscriber.loadItem(item)

    def goTo(self,item):
        for subscriber in self.__subscribers:
            subscriber.goTo(self.__currentItem,item)
        self.__currentItem = item

    def subscribe(self, subscriber):
        self.__subscribers.append(subscriber)
        subscriber.add(Root()) # telling my subscribers 'bout the OG

    def saveAs(self,fileName):

        bytes = []

        for subscriber in self.__subscribers:
            bytes += subscriber.saveState()

        # gotta know where I am when I get back
        bytes += encode(self.__currentItem.getID())

        bytes += save(self.__root)

        try:
            with open(fileName, "wb") as file:
                file.write(bytearray(bytes))
        except Exception as error:
            print("CRITICAL ERROR: ",error)

    def load(self,file):

        # clear out, there's a new guy in town
        self.clear()

        with open(file,"rb") as file:
            file = list(file.read())

        for subscriber in self.__subscribers:
            file = subscriber.setState(file)

        # I will remember you
        file,currentID = decode(file)

        justAdded = self.__root

        while len(file) != 0:

            match file.pop(0):
                case 0:
                    currentlyDecoding = Drawing()
                case 1:
                    currentlyDecoding = Line()
                case 2:
                    currentlyDecoding = Rectangle()
                case 3:
                    currentlyDecoding = Oval()


            file,parentID = decode(file)

            # finding their parent (because we recursively encode the file, we know we have already decoded their
            # parent and their parent is some parent of the thing we just added)
            while True:
                if justAdded.getID() == parentID:
                    justAdded.addChild(currentlyDecoding)
                    currentlyDecoding.setParent(justAdded)
                    break
                else:
                    justAdded = justAdded.getParent()

            justAdded = currentlyDecoding

            # this is when the class gets all the data it needs
            file = currentlyDecoding.decode(file)

            # I REMEMBER YOU!!! YOU'RE THE THING THAT'S CURRENT!
            if currentlyDecoding.getID() == currentID:
                current = currentlyDecoding

            # telling my subscribers
            self.loadItem(currentlyDecoding)

        # at the end of the loop
        self.goTo(current)
