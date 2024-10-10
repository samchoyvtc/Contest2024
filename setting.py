#Game setting
Size_y = 40
Size_x = 40
Animation = True
In_move_animation = True
TEN_STEPS_RANDOM = True
auto_replay = False

#Contant
up = 0
down = 1
left = 2
right = 3

# 0 = [[1]]
mold_size_dict = {1:0,2:1,4:4,8:7,16:10,32:13,64:16,128:19,256:22}
moldsize = [2,4,8,16,32,64,128,256]
seq_size_list = [1,2,4,8,16,32,64,128,256]

molds = [[[1]]]

#for local generate board settings
Network = False
using_random_molds_to_shuffle = True
random_mold_times = 100

#for setting board animation
timepause_eachstep = 0.5		  #timespace each animation
animate_creating_question = False #animation when generate question
animate_eachstep_sloving = False   #animation when each step
animate_eachrows_sloving = False   #animation when each row finished
boardshow_start_end = False       #animation when start and end

#ai settings
optimized_roll_pos_mark = 1
