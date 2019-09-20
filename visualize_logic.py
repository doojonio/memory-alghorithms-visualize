from graphics import *
from something import *
import time

WINDOW_NAME = "Window"
WINDOW_LENGHT = 800
WINDOW_WIDTH = 800
PAGE_LENGHT = 50
PAGE_WIDTH = 50

win = GraphWin(WINDOW_NAME, WINDOW_LENGHT, WINDOW_WIDTH)
class Gpage:
    page = Page(0)
    coord = Point(0,0)
    rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
    label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), page.id)
    def __init__(self, page, coord):
        self.page = page
        self._change(coord)
    def _change(self, coord):
        self.coord = coord
        self.rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
        self.label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), self.page.id)
    def draw(self, window):
        self.rect.draw(window)
        self.label.draw(window)
    def move(self, x, y):
        self.rect.move(x, y)
        self.label.move(x, y)
        
    

        

