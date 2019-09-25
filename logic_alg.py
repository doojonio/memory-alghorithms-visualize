
import random

BREAK_VALUE = 999

random.seed()

#Страница
class Page:
    id = 0
    fifo = 0
    rbit = 0
    def __init__(self, id):
        self.id = id
        rbit = 1

class Transfer:
    vr_t_ph = Page(BREAK_VALUE)
    ph_t_vr = Page(BREAK_VALUE)
    ph_t_eph = Page(BREAK_VALUE)
    def update(self, vr_t_ph , ph_t_vr, ph_t_eph = Page(BREAK_VALUE)):
        self.vr_t_ph = vr_t_ph
        self.ph_t_vr = ph_t_vr
        self.ph_t_eph = ph_t_eph
        print(self.vr_t_ph.id, ' ', self.ph_t_vr.id, ' ', self.ph_t_eph.id, ' ', self.ph_t_eph.rbit)
    def __init__(self, vr_t_ph, ph_t_vr, ph_t_eph = Page(BREAK_VALUE)):
        self.update(vr_t_ph, ph_t_vr, ph_t_eph)
        

#Память
class Memory:
    vr = []
    ph = []
    MAX_PAGE = 20
    MAX_FIFO = MAX_PAGE
    MAX_PH_SIZE = 10
    last_ch = Transfer(Page(BREAK_VALUE), Page(BREAK_VALUE))

    #Напечатать состояние памяти
    @classmethod
    def printMemory(cls):
        print("physic memory: (id, fifo num)")
        for page in cls.ph:
            print("({0}, {1})".format(page.id, page.fifo))
        print("virtual memory: (id, fifo num)")
        for page in cls.vr:
            print("({0}, {1})".format(page.id, page.fifo))
        return
    
    #Замещение страницы из физ. памяти на заданную из виртуальной методом FIFO
    @classmethod
    def fifoStep(cls, vr_page_index):
        old_page = Page(0)
        old_page.fifo = cls.MAX_FIFO
        new_page = Page(0)
        new_page.fifo = 0
        for page in cls.ph:
            if(page.fifo < old_page.fifo):
                old_page = page
        for page in cls.ph:
            if(page.fifo > new_page.fifo):
                new_page.fifo = page.fifo
        old_page_index = cls.ph.index(old_page)
        cls.vr.append(cls.ph.pop(old_page_index))
        appending_page = cls.vr.pop(vr_page_index)
        cls.last_ch.update(appending_page, old_page) #определяем какие страницы меняются
        appending_page.fifo = new_page.fifo + 1
        cls.ph.append(appending_page)
        for page in cls.ph:
            page.fifo = page.fifo - 1
    
    #Инициализировать память упорядоченными страничками
    @classmethod
    def initMemory(cls):
        cls.ph.clear()
        cls.vr.clear()
        for i in range(cls.MAX_PH_SIZE):
            app_page = Page(i)
            app_page.fifo = i
            cls.ph.append(app_page)
        for i in range(cls.MAX_PAGE - cls.MAX_PH_SIZE):
            cls.vr.append(Page(i + cls.MAX_PH_SIZE))

    @classmethod
    def secondChanceStep(cls, vr_page_index):
        old_page = Page(0)
        old_page.fifo = cls.MAX_FIFO
        old_page_index = 0
        new_page = Page(0)
        new_page.fifo = 0
        appending_page = Page(0)
        for page in cls.ph:
            if(page.fifo < old_page.fifo):
                old_page = page
        for page in cls.ph:
            if(page.fifo > new_page.fifo):
                new_page.fifo = page.fifo
        old_page_index = cls.ph.index(old_page)
        if old_page.rbit == 1:
            appending_page = cls.ph.pop(old_page_index)
            cls.last_ch = Transfer(Page(BREAK_VALUE), Page(BREAK_VALUE), appending_page)
            appending_page.rbit = 0
        else:
            cls.vr.append(cls.ph.pop(old_page_index))
            appending_page = cls.vr.pop(vr_page_index)
            cls.last_ch = Transfer(appending_page, old_page, Page(BREAK_VALUE)) #определяем какие страницы меняются
            Memory.initRbits()
        appending_page.fifo = new_page.fifo + 1
        cls.ph.append(appending_page)
        for page in cls.ph:
            page.fifo = page.fifo - 1
    @classmethod
    def initRbits(cls):
        for page in cls.ph[1::]:
            page.rbit = random.randrange(0,2,1)
    







        
        
    
            
            
