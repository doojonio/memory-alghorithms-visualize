from graphics import *
from logic_alg import *
import time
import random

#### PROGRAMM SETTINGS ###################################################
WINDOW_NAME = "Window"
WINDOW_LENGHT = 800
WINDOW_WIDTH = 800
PAGE_LENGHT = 50
PAGE_WIDTH = 50
PH_COORD = Point(100,100)
VR_COORD = Point(400, 100)
PH_LABEL = Text(Point(PH_COORD.x + 50, PH_COORD.y - 20), "PHYSIC MEMORY")
VR_LABEL = Text(Point(VR_COORD.x + 50, PH_COORD.y - 20), "VIRTUAL MEMORY")
TIME_SLEEP = .002
MOVE_STEP = 1.0
### ADDITIONAL LABEL CODES ###
FIFO = 1             ### FIFO ALGORITHM
BIT = 2              ### BIT REFERENCES
SC_CH = 3            ### SECOND CHANCE ALG
AFU = 4             ### LEAST FREQUANCY U
LRU = 5             ### LEAST R U
##########################################################################

class Gpage:
    page = Page(0)
    coord = Point(0,0)
    x = .0
    y = .0
    rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
    label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), page.id)
    al_p = Point(coord.x - PAGE_LENGHT, coord.y + PAGE_WIDTH/2)
    a_label = Text(al_p, '')    
    def __init__(self, page, coord = Point(0,0)):
        self.page = page
        self.coord = coord
        self.rect = Rectangle(coord, Point(coord.x + PAGE_LENGHT, coord.y + PAGE_WIDTH))
        self.label = Text(Point(coord.x + PAGE_LENGHT/2, coord.y + PAGE_WIDTH/2), self.page.id)
        self.al_p = Point(self.coord.x - PAGE_LENGHT, self.coord.y + PAGE_WIDTH/2)
        self.a_label = Text(self.al_p, '0')
    def draw(self, window):
        self.label.draw(window)
        self.rect.draw(window)
    def move(self, x, y):
        self.rect.move(x, y)
        self.label.move(x, y)
        self.a_label.move(x, y)
        self.coord = Point(self.coord.x + x, self.coord.y + y)
    def switch_alabel(self, alabel_code):
        if alabel_code == FIFO:
            self.a_label.setText(self.page.fifo)
        if alabel_code == BIT:
            self.a_label.setText("T:{} U:{}".format(self.page.el_time_s_us, self.page.ubit))
        if alabel_code == SC_CH:
            self.a_label.setText("R:{} F:{}".format(self.page.rbit, self.page.fifo))
        if alabel_code == AFU:
            self.a_label.setText("CALLS:{}".format(self.page.n_calls))
        if alabel_code == LRU:
            self.a_label.setText("EL.T.:{}".format(self.page.el_time_s_us))
        
    def draw_alabel(self, window):
        self.a_label.draw(window)
    def undraw_alabel(self):
        self.a_label.undraw()   
        
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
    def update_alabels(self, alabel_code):
        for gpage in self.gpages:
            gpage.switch_alabel(alabel_code)
    def draw_alabels(self, window):
        for gpage in self.gpages:
            gpage.a_label.draw(window)
    def getCoord(self):
        return self.gpages[0].coord
        
class Gtransfering:
    gph = Gmemory(PH_COORD, Memory.ph)
    gvr = Gmemory(VR_COORD, Memory.vr)
    alabel_code = FIFO
    window = None
    def __init__(self, alabel_code, window):
        self.alabel_code = alabel_code
        self.updateGmemory()
        self.window = window
    def draw(self):
        self.gph.draw(self.window)
        self.gph.draw_alabels(self.window)
        self.gvr.draw(self.window)
    def updateGmemory(self):
        self.gph = Gmemory(PH_COORD, Memory.ph)
        self.gph.update_alabels(self.alabel_code)
        self.gvr = Gmemory(VR_COORD, Memory.vr)
    def doTransfer(self):
        self.gph.update_alabels(self.alabel_code)
        if Memory.last_ch.ph_t_eph.id != Page(BREAK_VALUE).id:
            self.gph.choose_moving_p(Memory.last_ch.ph_t_eph.id)
            moving_ph_gpage = self.gph.gpages[self.gph.moving_p_index]
            ### TRANFERING PH TO THE END OF THE PH ### 
            moving_ph_gpage.undraw_alabel()
            Mover.xMove(moving_ph_gpage, PH_COORD.x + PAGE_LENGHT)
            Mover.yMove(moving_ph_gpage, PH_COORD.y + self.gph.size * PAGE_WIDTH)
            Mover.xMove(moving_ph_gpage, PH_COORD.x)
            temp_gpage = self.gph.pop(self.gph.moving_p_index)
            self.gph.append_gp(temp_gpage)
            self.gph.update_alabels(self.alabel_code)
            moving_ph_gpage.draw_alabel(self.window)
            ### ALL PAGES TO THE UP ###
            Mover.yMoveSlice(self.gph, 0, PH_COORD.y)
            return
        self.gph.choose_moving_p(Memory.last_ch.ph_t_vr.id)
        self.gvr.choose_moving_p(Memory.last_ch.vr_t_ph.id)
        moving_ph_gpage = self.gph.gpages[self.gph.moving_p_index]
        moving_vr_gpage = self.gvr.gpages[self.gvr.moving_p_index]
        ### TRANSFERING PH TO VR ###
        moving_ph_gpage.undraw_alabel()
        Mover.xMove(moving_ph_gpage, VR_COORD.x - PAGE_LENGHT)
        Mover.yMove(moving_ph_gpage, VR_COORD.y + PAGE_WIDTH * self.gvr.size)
        Mover.xMove(moving_ph_gpage, VR_COORD.x)   
        ### TRANSFERING VR TO PH ###
        Mover.xMove(moving_vr_gpage, PH_COORD.x + PAGE_LENGHT)
        Mover.yMove(moving_vr_gpage, PH_COORD.y + PAGE_WIDTH * self.gph.size)
        Mover.xMove(moving_vr_gpage, PH_COORD.x)
        ### ###
        moving_vr_gpage.switch_alabel(self.alabel_code)
        moving_vr_gpage.draw_alabel(self.window)
        self.gph.append_gp(self.gvr.pop(self.gvr.moving_p_index))
        self.gvr.append_gp(self.gph.pop(self.gph.moving_p_index))
        if self.gph.moving_p_index != 0:
            Mover.yMoveSlice(self.gph, self.gph.moving_p_index, self.gph.gpages[self.gph.moving_p_index - 1].coord.y + PAGE_WIDTH)       
        if self.gvr.moving_p_index != 0:
            Mover.yMoveSlice(self.gvr, self.gvr.moving_p_index, self.gvr.gpages[self.gvr.moving_p_index - 1].coord.y + PAGE_WIDTH)        
        ### STEP UP FOR ALL!!! ###
        Mover.yMoveSlice(self.gph, 0, PH_COORD.y)
        Mover.yMoveSlice(self.gvr, 0, VR_COORD.y)
        self.gph.update_alabels(self.alabel_code)

class Mover:
    @staticmethod
    def xMove(gpage, xVal):
        if(gpage.coord.x < xVal):
            while gpage.coord.x < xVal:
                gpage.move(MOVE_STEP, 0)
                time.sleep(TIME_SLEEP)
        else:
            while gpage.coord.x > xVal:
                gpage.move(-MOVE_STEP, 0)
                time.sleep(TIME_SLEEP)
    def yMove(gpage, yVal):
        if(gpage.coord.y < yVal):
            while gpage.coord.y < yVal:
                gpage.move(0, MOVE_STEP)
                time.sleep(TIME_SLEEP)
        else:
            while gpage.coord.y > yVal:
                gpage.move(0, -MOVE_STEP)
                time.slepp(TIME_SLEEP)
    def xMoveSlice(gmemory, since_index, xVal):
        if gmemory.gpages[since_index].coord.x < xVal:
            while gmemory.gpages[since_index].coord.x < xVal:
                gmemory.move_since(MOVE_STEP, 0, since_index)
                time.sleep(TIME_SLEEP)
        else:
            while gmemory.gpages[since_index].coord.x > xVal:
                gmemory.move_since(-MOVE_STEP, 0, since_index)
                time.sleep(TIME_SLEEP)
    def yMoveSlice(gmemory, since_index, yVal):
        if gmemory.gpages[since_index].coord.y < yVal:
            while gmemory.gpages[since_index].coord.y < yVal:
                gmemory.move_since(0, MOVE_STEP, since_index)
                time.sleep(TIME_SLEEP)
        else:
            while gmemory.gpages[since_index].coord.y > yVal:
                gmemory.move_since(0, -MOVE_STEP, since_index)
                time.sleep(TIME_SLEEP)

        

