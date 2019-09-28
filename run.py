from visualize_logic import *
from logic_alg import *
from graphics import *
import random

methodcode = {
    FIFO : Memory.fifoStep,
    SC_CH : Memory.secondChanceStep,
    LRU : Memory.lru,
    BIT : Memory.bitR,
    AFU : Memory.lfu,
    AFU+! : Memory.mfu
    }

def main():
    print("Codes of algorithm:\nFIFO: {}\nSECOND CHANCE: {}\nLRU: {}\nREFERENCE BIT: {}\nLFU: {}\nMFU: {}".format(FIFO, SC_CH, LRU, BIT, AFU, AFU+1))
    alg_code = int(input('YOUR CODE: '))
    win = GraphWin(WINDOW_NAME, WINDOW_LENGHT, WINDOW_WIDTH)
    PH_LABEL.draw(win)
    VR_LABEL.draw(win)
    Memory.initMemory()
    if(alg_code != AFU+1):
        gtrans = Gtransfering(alg_code, win)
    else:
        gtrans = Gtransfering(AFU, win)
    gtrans.draw()
    while not win.isClosed():
        methodcode[alg_code](random.randrange(0, Memory.MAX_VR_SIZE, 1))
        gtrans.doTransfer()
main()
