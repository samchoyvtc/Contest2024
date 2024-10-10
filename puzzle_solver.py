import numpy as np
import timeit
import time
from setting import*


def Searcher (gm, end_mark, water_mark):
    #Input variable:
    # target_board : The final state of the puzzle should look like
    # work_board : The current state of the moving board
    # end_mark : Indicate the current x-location of done moving piece
    #            It also indicate the x-location of the target piece on the target board
    # water_mark :  Indicate the current number of row finished arranging
    #               It also indicate the y-location of the target piece on the target board
    ###
    # Update Ver :
    # input Varibale target_board & work_board all in class gm

    q_brd_mark = gm.size_x_1 - end_mark
    target_element = gm.target_board[water_mark][q_brd_mark]
    w_brd_mark = gm.size_x_1                               #pointer for marking comparing position
    seq_size = 0
    report_seq_size = 0            #store the size of matching sub-sequence which match power of 2 size


    # Piority 1 (Red zone)
    # Finding matching piece from the top row

    while q_brd_mark >= 0 and w_brd_mark >= end_mark:
        if target_element != gm.working_board[0][w_brd_mark]:
            w_brd_mark-=1
        else:
            report_w_brd_mark = w_brd_mark
            while target_element == gm.working_board[0][w_brd_mark] and w_brd_mark >= end_mark and q_brd_mark >= 0 :
                seq_size += 1
                w_brd_mark-= 1
                q_brd_mark-= 1
                if seq_size in seq_size_list:
                    report_seq_size = seq_size
                target_element = gm.target_board[water_mark][q_brd_mark]
            return report_seq_size,report_w_brd_mark,1



    # Piority 2  (Orange zone)
    # Target matching piece couldnt be found in the first row
    # Try to find it from the first column
    for y in range(1, gm.size_y - water_mark): 
        if gm.working_board[y][0] == gm.target_board[water_mark][q_brd_mark]:
            return 0,y,2


    # Piority 3 (Yellow zone)
    # Target matching piece couldnt be found neither in the first row or in the first column
    # Try to find it from the rest of the board
    for x in range(end_mark,gm.size_x): 
        for y in range(1, gm.size_y - water_mark):
            if gm.working_board[y][x] == gm.target_board[water_mark][q_brd_mark]:
                return x,y,3

    # Piority 4 (Green zone)
    # Target matching piece under the working mark
    for y in range(1, gm.size_y - water_mark):
        for x in range(1,end_mark):
            if gm.working_board[y][x] == gm.target_board[water_mark][q_brd_mark]:
                return x,y,4     
 

def solver(gm):

    start_time = time.time()
    gm.ai0_save = []
    pev_method = 0
    count = 0
    
    for y in range(gm.size_y):
        end_mark = 0
        while end_mark < gm.size_x:
            p1,p2,solutions = Searcher(gm,end_mark,y)
            if solutions == 1:  #(Red zone)   
                gm.moveit(mold_size_dict[p1],  p2-p1+1, 1-p1,right,0)
                end_mark += p1      #After moving board, mark how many pieces have been moved
                count += 1

            if solutions == 2:  #(Orange zone)  
                #Move one piece from top row toward (0,0) to make a space
                gm.moveit(0, gm.size_x_1, 0, right,0)
                count += 1

                #Move the matching piece upward toward (0,0)
                gm.moveit(0, p1, p2 ,down,0)
                end_mark += 1      #After moving board, mark how many pieces have been moved
                count += 1

            if solutions == 3:   #(Yellow zone)

                #Move the matching piece upward to the top row
                gm.moveit(0, p1, p2 ,down,0)
                count += 1

                #Move the top row matching piece toward (0,0)
                gm.moveit(0,p1,0,right,0)
                end_mark += 1      #After moving board, mark how many pieces have been moved
                count += 1

            if solutions == 4:   #(Green zone) #fixed the xy bug from solutions 4 

                #Move the matching piece left way to the first column
                gm.moveit(0, p1, p2 ,left,0)
                count += 1

                #Move one piece from top row toward (0,0) to make a space
                gm.moveit(0,gm.size_x_1,p2, down,0)
                count += 1

                #Move the matching piece upward toward (0,0)
                gm.moveit(0,gm.size_x_1,0,right,0)
                end_mark += 1      #After moving board, mark how many pieces have been moved
                count += 1
       
            
            

        #After finishing one row, move the whole row to the bottom
        gm.moveit(22, 0, -255 ,up,0)
        count+=1         
        #Show summary for each row
        nowtime = time .time() 
        print("time: ",nowtime-start_time , " Seconds")
        progress = (y / (gm.size_y_1)) * 100
        print(f"count = {count} times")
        print("已完成：{:.2f}%".format(progress))

    return count



