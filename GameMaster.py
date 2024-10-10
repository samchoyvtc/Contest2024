import random 
import question_generator
import copy
import numpy as np
import setting
from setting import*
import time
from server_api import*
from scipy.optimize import linear_sum_assignment
from collections import Counter

 

class gameboard():
    def __init__(self) :
        self.question_save = []
        self.ai_save = []
        self.board_diffrent = []
        self.puzzle_row_matching = []
        self.saveboard = False
        self.row_diffrent = []
        self.marking_board = []
        if Network == True:
            self.generator = question_generator.puzzle_generator(self)
            self.size_x,self.size_y,self.working_board ,self.target_board, self.pattern_dict= server_get()
            self.initial_board = copy.deepcopy(self.working_board)
            self.size_x_1 = self.size_x-1
            self.size_y_1 = self.size_y-1
            for moremold in range (len(self.pattern_dict)):
                molds.append(self.pattern_dict[f"{moremold + 25}"])
        if Network == False:
            self.size_x,self.size_y = Size_x,Size_y
            self.saveboard = True
            self.generator = question_generator.puzzle_generator(self)
            self.saveboard = False
            self.initial_board = copy.deepcopy(self.working_board)
            self.size_x_1 = self.size_x-1
            self.size_y_1 = self.size_y-1
        self.compareboard()
        self.optimized_roll()
        self.row_compare()

    def optimized_roll(self):

        matchlist = []
        match_place_list = []
        tb_num_counts=[]
        match_row_list = []
        for i in range(self.size_y):
            match_row_list.append([])
            
        for ans_row in self.target_board:
            tb_num_counts.append(Counter(ans_row))
            
        for j, each_row in enumerate(self.working_board):
            wb_num_count=Counter(each_row)
            matchlist.append([])
            for idx ,tb_count in enumerate(tb_num_counts):
                match_count = 0
                for num in wb_num_count:
                    if num in tb_count:
                        match_count += min(wb_num_count[num],tb_count[num])
                ptr = self.size_x-1
                while self.working_board[j][ptr] == self.target_board[idx][ptr] and ptr != -1:
                    match_count += optimized_roll_pos_mark
                    ptr -= 1                        
                matchlist[j].append(match_count)  
        cost = -np.array(matchlist)
        row, col = linear_sum_assignment(cost)
        max_sum = -cost[row, col].sum()
        self.puzzle_row_matching = col.tolist()   
        print(np.array(matchlist))
        print(self.puzzle_row_matching)

    def row_compare(self):
        self.marking_board = [[0 for  i in range(self.size_x)]for j in range(self.size_y)]
        print(np.array(self.working_board),np.array(self.target_board))
        for idx ,row in enumerate(self.working_board):
            tb_count = Counter(self.target_board[self.puzzle_row_matching[idx]])
            wb_count = Counter(row)
            for num in tb_count:
                x = self.size_x-1
                for i in range(min(wb_count[num],tb_count[num])):
                    print(np.array(self.marking_board))
                    print("i",i,num,idx)
                    while row[x] != num:
                        x -= 1
                    self.marking_board[idx][x] = 1
                    x-=1

        for y in range (self.size_y):
            for x in range(self.size_x):
                if self.working_board[y][x] == self.target_board[self.puzzle_row_matching[y]][x] and self.marking_board[y][x] == 1:
                   # print(x,y,self.working_board[y][x],self.target_board[self.puzzle_row_matching[y]][x])
                    self.marking_board[y][x] +=1
                    #print(np.array(self.marking_board))

        print(np.array(self.marking_board))

    def compareboard(self):
        for i in range(self.size_y):
            board_diffrent_save = []
            for j in range(self.size_x):
                if self.working_board[i][j] == self.target_board[i][j]:
                    board_diffrent_save.append(1)
                else:
                    board_diffrent_save.append(0)

            self.board_diffrent.append(board_diffrent_save)

    def mark_moving_piece (self,mold_no, mark_board, x, y):
        mold = setting.molds[mold_no]
        if x <= 0:
            str_x = 0
        else:
            str_x = x
            
        end_x = len(mold[0]) + x
        if end_x > self.size_x:
            end_x = self.size_x

        if y <= 0:
            str_y = 0
        else:
            str_y = y

        end_y = len(mold) + y
        if end_y > self.size_y:
            end_y = self.size_y

        for loc_y in range(str_y, end_y):
            for loc_x in range(str_x, end_x):
                mark_board[loc_y][loc_x] = mold[loc_y - y][loc_x - x]
        return str_x, str_y, end_x, end_y,mark_board

    def moveit (self,mold, x , y, direction,algorthim_no):

        mark_board = [[0]*self.size_x for i in range(self.size_y)]


        str_x, str_y, end_x, end_y ,mark_board= self.mark_moving_piece(mold, mark_board, x, y)




        if direction == right or direction == left: #easy horizontal movment (right & left)
            for row in range(str_y , end_y):
                temp_list = []
                for loc_x in range(str_x, end_x):
                    if mark_board[row][loc_x] == 1:
                        temp_list.append(self.working_board[row].pop(loc_x-len(temp_list)))
                if direction == left: # left
                    self.working_board[row].extend(temp_list)   
                else:              # right
                    self.working_board[row][0:0] = temp_list
        else: #down or up
            
            for loc_x in range(str_x , end_x):
                temp_list_0 = [] # for marked by mold 0
                temp_list_1 = [] # for marked by mold 1
                for row in range(self.size_y):
                    if mark_board[row][loc_x] == 1:
                        temp_list_1.append(self.working_board[row][loc_x])
                    else:
                        temp_list_0.append(self.working_board[row][loc_x])
                if direction == down: # down
                    for a in range (len(temp_list_1)):
                        self.working_board[a][loc_x] = temp_list_1[a]
                    for i,b in enumerate(range(len(temp_list_1), self.size_y)):
                        self.working_board[b][loc_x] = temp_list_0[i]
                else: # up (no.1)
                    for a in range (len(temp_list_0)):
                        self.working_board[a][loc_x] = temp_list_0[a]
                    for i,b in enumerate(range(len(temp_list_0), self.size_y)):
                        self.working_board[b][loc_x] = temp_list_1[i]
        if self.saveboard == True:
            self.saveit(mold, x , y, direction, algorthim_no)

    def saveit (self,mold, x , y, direction,ai):
        load = []

        if ai == "question":
            load.append(mold)
            load.append(x)
            load.append(y)
            load.append(direction)
            self.question_save.append(load)
        else:
            load.append(mold)
            load.append(x)
            load.append(y)
            load.append(direction)
            self.ai_save[ai].append(load)
            
    def deleteit(self,ai):
        self.ai_save[ai].pop()
    
    def resetboard(self):
        self.working_board = copy.deepcopy(self.initial_board)