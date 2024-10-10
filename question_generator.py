import random
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import time
from setting import *
import makemold


class puzzle_generator():
    def __init__(self,parent):
        self.molds_maker()
        if Network == False:
            board = self.board_generator ()
            parent.working_board = deepcopy(board)
            parent.target_board = deepcopy(board)
            self.target_generator(parent) 
            parent.target_board = deepcopy(parent.working_board)
            parent.working_board = deepcopy(board)

    def molds_maker(self):
        for boxsize in moldsize:
            for boxtype in range(3):
                molds.append(makemold.mold_boxes(boxsize,boxtype))

    def board_generator(self ):
        board = []
        for i in range(Size_y):
            g = []
            for j in range(Size_x):
                Random_num = random.randint(0,3)
                g.append(Random_num)
            board.append(g)
        return board

    def target_generator(self,parent):
        if using_random_molds_to_shuffle == True:
            for i in range(random_mold_times):
                random_location = random.randint(0,3)
                random_y = random.randint(0,Size_x-1)
                random_x = random.randint(0,Size_y-1)
                random_moldtype = random.randint(0,24)
                parent.moveit(random_moldtype,random_x,random_y,random_location,"question")
        parent.boardshow_start_end = False
