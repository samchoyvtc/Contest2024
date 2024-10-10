import numpy as np
import timeit
import time
from setting import*
from collections import Counter
 

def optimized_roll(gm):

    cost = -np.array(gm.working_board)

    print(cost)

    row, col = linear_sum_assignment(cost)

    # Calculate the maximum sum and selected numbers
    max_sum = -cost[row, col].sum()

    self.puzzle_row_matching = col.tolist   
    print(self.puzzle_row_matching)

    return 