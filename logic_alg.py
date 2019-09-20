#Страница
class Page:
    def __init__(self, id):
        self.id = id
    id = 0
    fifo = 0

#Память
class Memory:
    vr = list()
    ph = list()
    MAX_PAGE = 10
    MAX_FIFO = 9999
    MAX_PH_SIZE = 5

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









        
        
    
            
            
