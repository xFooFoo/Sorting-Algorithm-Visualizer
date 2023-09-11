from typing import List
import random
import numpy as np
import time
import textwrap
import pygame


def bubblesort(data: List[int]):
    n = len(data)
    for run in range(0,n):
        for counter in range(0,n - run - 1): #minus one since it checks value on RHS index is +1 in if-statement
            if data[counter] > data[counter + 1]:
                data[counter + 1], data[counter] = data[counter] , data[counter + 1] #swap
                print(f"Run {run+1}, Step {counter+1}: {data}") #Prints each step for visualization
                #Updates plot every swap with a delay
                update_plot(data)

#PLOT FOR IN-PLACE ALGORITHMS
def update_plot(data: List[int]):
    for i in range(0, len(data)):
        pygame.draw.rect(screen, purpleBlock, (i * float(SCREEN_WIDTH/DATA_SIZE), float(SCREEN_HEIGHT - data[i]), float(SCREEN_WIDTH/DATA_SIZE), data[i]) )
        #Delay necessary to see each update
        pygame.time.delay(0.3)


# Generate a list of 10 random numbers
DATA_SIZE = 25
MAX_VALUE = 100
random_numbers = [random.randint(1, MAX_VALUE) for _ in range(DATA_SIZE)]

#TESTING CODE
bubblesort(random_numbers)
output = random_numbers
#Test whether algorithm sorts properly
if output == sorted(random_numbers):
    print("The list has been sorted.")
else:
    print(output)
    print(sorted(random_numbers))
plt.show() #SHOWS ALL DRAWINGS

