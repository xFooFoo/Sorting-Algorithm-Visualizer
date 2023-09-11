from typing import List
import random
import numpy as np
import math
import time
import textwrap
import pygame


def bubblesort(data: List[int]):
    n = len(data)
    plotting = True
    while plotting: #while-loop is for user's early stoppage
        for run in range(0,n):
            for counter in range(0,n - run - 1): #minus one since it checks value on RHS index is +1 in if-statement
                if data[counter] > data[counter + 1]:
                    data[counter + 1], data[counter] = data[counter] , data[counter + 1] #swap
                    print(f"Run {run+1}, Step {counter+1}: {data}") #Prints each step for visualization
                    #Plot/Screen updates
                    update_plot(data)
                    
        #When algorithm finishes
        plotting = False

#PLOT FOR IN-PLACE ALGORITHMS
#, text_surface: pygame.Surface, text_rect: pygame.Rect
def update_plot(data: List[int]):
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    # Draws the title
    screen.blit(text_surface, text_rect)
    # Draws each data as a block
    for i in range(0, len(data)):
        pygame.draw.rect(screen, purpleBlock, (i * (SCREEN_WIDTH/DATA_SIZE) + UI_WIDTH_PADDING/2, SCREEN_HEIGHT + UI_HEIGHT_PADDING/2 - data[i] , SCREEN_WIDTH/DATA_SIZE, data[i]))
        #Delay necessary to see each update
        pygame.time.delay(1) #make this customizable
    pygame.display.flip()

def reset():
    random_numbers = [random.randint(1, MAX_VALUE) for _ in range(DATA_SIZE)]

def create_title(title: str):
    # Create a font object
    font = pygame.font.Font(None, 36)  # You can specify a font file or use None for a default font
    text_surface  = font.render(title, True, purpleBlock)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH + UI_WIDTH_PADDING) / 2, UI_HEIGHT_PADDING/4)
    return text_surface, text_rect

# Generate a list of random numbers
DATA_SIZE = 100 #make this customizable & keep them even to prevent rounding errors when drawing & positioning
MAX_VALUE = 800 #Anything greater than screen_height would go over the frame...
random_numbers = [random.randint(1, MAX_VALUE) for _ in range(DATA_SIZE)]
print(f"{random_numbers}")

#Pygame setup
UI_WIDTH_PADDING = 50
UI_HEIGHT_PADDING = 200
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
purpleBlock =  pygame.Color(67, 1, 135, 255)
pygame.init()
pygame.display.set_caption("Sorting Algorithm Visualizer")
screen = pygame.display.set_mode((SCREEN_WIDTH + UI_WIDTH_PADDING , SCREEN_HEIGHT + UI_HEIGHT_PADDING))
clock = pygame.time.Clock()


running = True
plotting = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            plotting = False

    # RENDER YOUR GAME HERE
    text_surface, text_rect = create_title("Bubblesort")
    bubblesort(random_numbers)

    clock.tick(60)  # limits FPS to 60

pygame.quit()

#TESTING CODE

output = random_numbers
#Test whether algorithm sorts properly
if output == sorted(random_numbers):
    print("The list has been sorted.")
else:
    print(output)
    print(sorted(random_numbers))


