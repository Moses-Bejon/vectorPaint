from tkinter import *

class Shape():
    def __init__(self,root_frame, place):
        self._root_frame = root_frame
        self._place = place
    def continue_draw(self,event):
        coords_list = self._root_frame.coords(self._geometry)
        if event.x > self._place[0]:
            coords_list[0] = self._place[0]
            coords_list[2] = event.x
        else:
            coords_list[2] = self._place[0]
            coords_list[0] = event.x
        if event.y > self._place[1]:
            coords_list[1] = self._place[1]
            coords_list[3] = event.y
        else:
            coords_list[3] = self._place[1]
            coords_list[1] = event.y
        self._root_frame.coords(self._geometry, coords_list)

class Line(Shape):
    def __init__(self, root_frame, event, colour):
        super().__init__(root_frame,(event.x,event.y))
        self._geometry = self._root_frame.create_line(event.x, event.y, event.x, event.y, fill=colour)
    def continue_draw(self,event):
        coords_list = self._root_frame.coords(self._geometry)
        coords_list[2] = event.x
        coords_list[3] = event.y
        self._root_frame.coords(self._geometry, coords_list)

class Rectangle(Shape):
    def __init__(self, root_frame, event, colour):
        super().__init__(root_frame,(event.x,event.y))
        self._geometry = self._root_frame.create_rectangle(event.x, event.y, event.x, event.y, fill=colour)
