import time
import random

BREAK_VALUE = 999

random.seed()

#Страница
class Page:
    id = 0
    fifo = 0
    rbit = random.randrange(0,2,1)
    ubit = random.randrange(0,2,1)
    n_calls = random.randrange(0, 666, 1)
    el_time_s_us = random.randrange(0, 666, 1)
    def __init__(self, id):
        self.id = id

class Transfer:
    vr_t_ph = Page(BREAK_VALUE)
    ph_t_vr = Page(BREAK_VALUE)
    ph_t_eph = Page(BREAK_VALUE)
    def update(self, vr_t_ph , ph_t_vr, ph_t_eph = Page(BREAK_VALUE)):
        self.vr_t_ph = vr_t_ph
        self.ph_t_vr = ph_t_vr
        self.ph_t_eph = ph_t_eph
    def __init__(self, vr_t_ph, ph_t_vr, ph_t_eph = Page(BREAK_VALUE)):
        self.update(vr_t_ph, ph_t_vr, ph_t_eph)
        

#Память
class Memory:
    vr = []
    ph = []
    MAX_PAGE = 20
    MAX_FIFO = MAX_PAGE
    MAX_PH_SIZE = 10
    MAX_VR_SIZE = MAX_PAGE - MAX_PH_SIZE
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
        cls.last_ch = Transfer(appending_page, old_page) #определяем какие страницы меняются
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
            cls.initRandomValues()
        appending_page.fifo = new_page.fifo + 1
        cls.ph.append(appending_page)
        for page in cls.ph:
            page.fifo = page.fifo - 1
    @classmethod
    def initRandomValues(cls):
        for page in cls.ph[1::]:
            page.rbit = random.randrange(0,2,1)
            page.el_time_s_us = random.randrange(0, 666, 1)
            page.ubit = random.randrange(0, 2, 1)
            page.n_calls = random.randrange(0, 666, 1)
    @classmethod
    def bitR(cls, vr_page_index):
        exit_page = cls.ph[0]
        for page in cls.ph:
            if (exit_page.el_time_s_us < page.el_time_s_us) and (page.ubit == 0):
                exit_page = page
        exit_page_index = cls.ph.index(exit_page)
        cls.approve_transfer(vr_page_index, exit_page_index)
        cls.initRandomValues()
    @classmethod
    def lfu(cls, vr_page_index):
        exit_page = cls.ph[0]
        for page in cls.ph:
            if exit_page.n_calls > page.n_calls:
                exit_page = page
        exit_page_index = cls.ph.index(exit_page)
        cls.approve_transfer(vr_page_index, exit_page_index)
        cls.initRandomValues()
    @classmethod
    def approve_transfer(cls, vr_page_index, ph_page_index):
        vr_page = cls.vr.pop(vr_page_index)
        ph_page = cls.ph.pop(ph_page_index)
        cls.vr.append(ph_page)
        cls.ph.append(vr_page)
        cls.last_ch = Transfer(vr_page, ph_page)
    @classmethod
    def lru(cls, vr_page_index):
        exit_page = cls.ph[0]
        for page in cls.ph:
            if exit_page.el_time_s_us < page.el_time_s_us:
                exit_page = page
        cls.approve_transfer(vr_page_index, cls.ph.index(exit_page))
        cls.initRandomValues()
    @classmethod
    def mfu(cls, vr_page_index):
        exit_page = cls.ph[0]
        for page in cls.ph:
            if exit_page.n_calls < page.n_calls:
                exit_page = page
        exit_page_index = cls.ph.index(exit_page)
        cls.approve_transfer(vr_page_index, exit_page_index)
        cls.initRandomValues()
        

    




        
        
    
            
            
