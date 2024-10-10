import random
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import time
import timeit
import GameMaster
import puzzle_solver
import setting 
from server_api import*
import tkinter as tk
from GraphicUserInterface import GUI
import optimized_roll

GM = GameMaster.gameboard()
root = tk.Tk()
UserInterface = GUI(root,GM)
GM.ai_save = [[]*100]

def gui_update():
    root.update()

#Flow control
while True:
    gui_update()
    if UserInterface.state == 0:        #guiupdate
        continue

    elif UserInterface.state == 1:      #algorthim 1
        GM.saveboard = True
        GM.resetboard()
        puzzle_solver.solver(GM)
        UserInterface.algorithm_steps[0] = len(GM.ai_save[0])
        UserInterface.create_buttons(GM)
        GM.saveboard = False
        UserInterface.state = 0
        UserInterface.post_btns[0]["state"] = "enable"
        
    elif UserInterface.state == 2:      #post algorthim1 ans
        if Network:
            GameMaster.server_post(GM.ai_save[0])
        animate_step_stalling = deepcopy(GM.ai_save[0])
        UserInterface.state = 9999
        

    elif UserInterface.state == 999:        #replay question
        animate_step_stalling = deepcopy(GM.question_save)
        UserInterface.state = 9999

    elif UserInterface.state == 9999:      #animation after post
        GM.resetboard()
        UserInterface.plot_update(GM)
        if auto_replay or animate_step_stalling != GM.question_save:
        
            for i in animate_step_stalling:
                GM.moveit(i[0],i[1],i[2],i[3],"")
                UserInterface.plot_update(GM)
                gui_update()
                time.sleep(0.1)
            UserInterface.state = 0
            if animate_step_stalling == GM.question_save:
                time.sleep(3)
                GM.resetboard()
                UserInterface.plot_update(GM)
        else:
            UserInterface.reset_animationstep()
            UserInterface.state = 9998

    elif UserInterface.state == 9998:    
        time.sleep(0.1)
        
    elif UserInterface.state == 9997:    
        if UserInterface.animation_step == len(animate_step_stalling):
            UserInterface.state = 0
            UserInterface.post_btns[5]["state"] = "disabled"
            UserInterface.post_btns[4]["state"] = "enabled" 
            GM.resetboard()
            UserInterface.plot_update(GM)
        else:
            i = animate_step_stalling[UserInterface.animation_step] 
            GM.moveit(i[0],i[1],i[2],i[3],"")
            UserInterface.plot_update(GM)
            gui_update()
            UserInterface.state = 9998

        
