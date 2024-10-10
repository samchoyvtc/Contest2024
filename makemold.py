import numpy as np
import matplotlib.pyplot as plt
import time
from setting import*


def mold_boxes(Size,Type ):
    mold = []
    if Size == 0:
        mold.append([1])
    elif Type == 0 :  # full size
        for i in range(Size):
            row_of_mold = []
            for j in range(Size):
                row_of_mold.append(1)
            mold.append(row_of_mold)

    elif Type == 1 :  # horizontal skipping
        round = 0
        for i in range(Size):
            row_of_mold = []
            if round%2 == 0:
                for j in range(Size):
                    row_of_mold.append(1)
                mold.append(row_of_mold)
                round += 1
            else:
                for j in range(Size):
                    row_of_mold.append(0)
                mold.append(row_of_mold)
                round += 1   
            
    elif Type == 2 :  # vertical skipping

        for i in range(Size):
            row_of_mold = []
            round = 0
            for j in range(Size):
                if round % 2 == 0 :
                    row_of_mold.append(1)
                    round += 1
                else:
                    row_of_mold.append(0)
                    round += 1
            mold.append(row_of_mold)

    return mold

def get_molds_from_network():
    return True


def prepare_molds():
    if Network:
        get_molds_from_network()
