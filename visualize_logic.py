from graphics import *
from logic_alg import *
import time
import random

WINDOW_NAME = "Window"
WINDOW_LENGHT = 800
WINDOW_WIDTH = 800
PAGE_LENGHT = 50
PAGE_WIDTH = 50
PH_COORD = Point(50,50)
VR_COORD = Point(300, 50)
PH_LABEL = Text(Point(PH_COORD.x + 50, PH_COORD.y - 20), "PHYSIC MEMORY")
VR_LABEL = Text(Point(VR_COORD.x + 50, PH_COORD.y - 20), "VIRTUAL MEMORY")

win = GraphWin(WINDOW_NAME, WINDOW_LENGHT, WINDOW_WIDTH)
PH_LABEL.draw(win)
VR_LABEL.draw(win)
TIME_SLEEP = .002
MOVE_STEP = 1.0

class Gpage:
    page = Page(0)
    coord = Point(0,0)
    x = .0
    y = .0
    rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
    label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), page.id)
    def __init__(self, page, coord = Point(0,0)):
        self.page = page
        self.coord = coord
        self.rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
        self.label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), self.page.id)        
    def draw(self, window):
        self.label.draw(window)
        self.rect.draw(window)
    def move(self, x, y):
        self.rect.move(x, y)
        self.label.move(x, y)
        self.coord = Point(self.coord.x + x, self.coord.y + y)
        

class Gmemory:
    gpages = list()
    coord = Point(0,0)
    size = 0
    moving_p_index = 0
    def __init__(self, coord, pages):
        self.coord = coord
        self.gpages = list()
        for page in pages:
            self.append(page)
    def append(self, page):
        self.gpages.append(Gpage(page, Point(self.coord.x, self.coord.y + self.size * PAGE_WIDTH)))
        self.size = 1 + self.size
    def append_gp(self, gpage):
        self.gpages.append(gpage)
        self.size = 1 + self.size
    def pop(self, gp_index):
        self.size = self.size - 1
        return self.gpages.pop(gp_index)
    def draw(self, window):
        for gpage in self.gpages:
            gpage.draw(window)
    def move(self, x, y):
        for gpage in self.gpages:
            gpage.move(x, y)
    def choose_moving_p(self, id):
        for gpage in self.gpages:
            if(gpage.page.id == id):
                self.moving_p_index = self.gpages.index(gpage)
                return
    def move_page(self, x, y):
        self.gpages[self.moving_p_index].move(x, y)
    def move_since(self, x, y, start):
        for gpage in self.gpages[start::1]:
            gpage.move(x, y)

class Gtransfering:
    gph = Gmemory(PH_COORD, Memory.ph)
    gvr = Gmemory(VR_COORD, Memory.vr)
    def __init__(self):
        self.updateGmemory()
    def draw(self, window):
        self.gph.draw(window)
        self.gvr.draw(window)
    def updateGmemory(self):
        self.gph = Gmemory(PH_COORD, Memory.ph)
        self.gvr = Gmemory(VR_COORD, Memory.vr)
    def doTransfer(self):
        self.gph.choose_moving_p(Memory.last_ch.ph_t_vr.id)
        self.gvr.choose_moving_p(Memory.last_ch.vr_t_ph.id)
        moving_ph_gpage = self.gph.gpages[self.gph.moving_p_index]
        moving_vr_gpage = self.gvr.gpages[self.gvr.moving_p_index]
        ### TRANSFERING PH TO VR ###
        while moving_ph_gpage.coord.x < VR_COORD.x - PAGE_LENGHT:
            self.gph.move_page(MOVE_STEP,0)
            time.sleep(TIME_SLEEP)
        while moving_ph_gpage.coord.y < VR_COORD.y + PAGE_WIDTH * self.gvr.size:
            self.gph.move_page(0, MOVE_STEP)
            time.sleep(TIME_SLEEP)
        while moving_ph_gpage.coord.x < VR_COORD.x:
            self.gph.move_page(MOVE_STEP,0)
            time.sleep(TIME_SLEEP)
        ### TRANSFERING VR TO PH ###
        while moving_vr_gpage.coord.x > PH_COORD.x + PAGE_LENGHT:
            self.gvr.move_page(-MOVE_STEP,0)
            time.sleep(TIME_SLEEP)
        while moving_vr_gpage.coord.y < PH_COORD.y + PAGE_WIDTH * self.gph.size:
            self.gvr.move_page(0, MOVE_STEP)
            time.sleep(TIME_SLEEP)
        while moving_vr_gpage.coord.x > PH_COORD.x:
            self.gvr.move_page(-MOVE_STEP, 0)
            time.sleep(TIME_SLEEP)
        ### ###
        self.gph.append_gp(self.gvr.pop(self.gvr.moving_p_index))
        self.gvr.append_gp(self.gph.pop(self.gph.moving_p_index))
        if self.gph.moving_p_index != 0:
            while self.gph.gpages[self.gph.moving_p_index].coord.y > self.gph.gpages[self.gph.moving_p_index - 1].coord.y + PAGE_WIDTH:
                for gpage in self.gph.gpages[self.gph.moving_p_index::1]:
                    gpage.move(0,-MOVE_STEP)
                    time.sleep(TIME_SLEEP)
        if self.gvr.moving_p_index != 0:
            while self.gvr.gpages[self.gvr.moving_p_index].coord.y > self.gvr.gpages[self.gvr.moving_p_index - 1].coord.y + PAGE_WIDTH:
                    self.gvr.move_since(0, -MOVE_STEP, self.gvr.moving_p_index)
                    time.sleep(TIME_SLEEP)
        ### STEP UP FOR ALL!!! ###
        while self.gph.gpages[0].coord.y > PH_COORD.y:
            self.gph.move(0, -MOVE_STEP)
            time.sleep(TIME_SLEEP)
        while self.gvr.gpages[0].coord.y > VR_COORD.y:
            self.gvr.move(0, -MOVE_STEP)
            time.sleep(TIME_SLEEP)
            
Memory.initMemory()
gtrans = Gtransfering()
gtrans.draw(win)
random.seed()
for _ in range(999):
    Memory.fifoStep(random.randrange(0,9,1))
    gtrans.doTransfer()
win.close()

        

