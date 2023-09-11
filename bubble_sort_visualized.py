from typing import List
import random
import numpy as np
import time
import textwrap
import pygame


#Bubble sort returns an iterator of the values in data FOR EACH iteration
def bubblesort(data: List[int]):
    n = len(data)
    for run in range(0,n):
        for counter in range(0,n - run - 1): #minus one since it checks value on RHS index is +1 in if-statement
            if data[counter] > data[counter + 1]:
                data[counter + 1], data[counter] = data[counter] , data[counter + 1] #swap
                print(f"Run {run+1}, Step {counter+1}: {data}") #Prints each step for visualization
                yield data
