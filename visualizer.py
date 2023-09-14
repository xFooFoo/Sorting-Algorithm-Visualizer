from typing import List
import random
import numpy as np
import math
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

def insertion_sort(data: List[str]):
    n = len(data)
    for i in range(1,n):
        for j in range(i, 0, -1):
            if data[j-1] > data[j]:
                data[j], data[j-1] = data[j-1], data[j]
                print(data)
            yield data

def selection_sort(data: List[int]):
    n = len(data)
    for i in range(1,n):
        min_tup = (i-1,data[i-1]) #key,val in a tuple
        for j in range(i,n): #last iteration n to n ignored since it must be the largest left over in the last position
            if data[j] < min_tup[1]:
                min_tup = (j, data[j]) #minimum value in unsorted position
            print(data)
        data[min_tup[0]], data[i-1] = data[i-1] ,min_tup[1] #swap value of the ith position with the minimum value
        yield data

def quicksort(data: List[int], low: int, high: int):
    print(f"data {data}, low {low}, high {high}")
    if low >= high:
        return
    left = low
    right = high
    medianIndex = (high + low)//2
    pivot = data[medianIndex]
    print(f"pivot {pivot}")
    #place pivot to the last position, vice versa
    data[medianIndex] = data[high]
    data[high] = pivot
    yield data
    right -= 1
    print(f"Move pivot to end {data}")
    while (left <= right):
        if data[left] > pivot:
            if data[right] <= pivot: #moves the right index to the left even on same value to action the swap. This causes quicksort to be unstable.
                temp = data[left]
                print(f"Found {data}, left {left}, right {right}")
                data[left] = data[right] 
                data[right] = temp
                left += 1
                right -= 1
                print(f"Swap {data}, left {left}, right {right}")
            else:
                right -= 1
        else:
            left += 1
        yield data
    #Final swap to put pivot in its correct pos
    data[high] = data[left] #high is now left of left, and left is right of right and Pivot value > Left value so we place Pivot on the right of the left value
    data[left] = pivot
    print(f"Pivot back {data}, left {left}, right {right}")
    yield data
    #recursion on LHS & RHS of the pivot
    yield from quicksort(data, low, left - 1)
    yield from quicksort(data, left + 1, high)

#PLOT FOR IN-PLACE ALGORITHMS
def update_plot(data: List[int], title: str):
    title_surface, title_rect = create_textbox(title, purpleBlock, (SCREEN_WIDTH + UI_WIDTH_PADDING) / 2, UI_HEIGHT_PADDING/4, titleFont)
    # Draws the title
    screen.blit(title_surface, title_rect)
    global comparisons 
    comparisons += 1
    # Draws each data as a block
    for i in range(0, len(data)):
        pygame.draw.rect(screen, purpleBlock, (i * (SCREEN_WIDTH/DATA_SIZE) + UI_WIDTH_PADDING/2, SCREEN_HEIGHT + UI_HEIGHT_PADDING/2 - data[i] , SCREEN_WIDTH/DATA_SIZE, data[i]))
        #Delay necessary to see each update
        pygame.time.delay(DELAY_IN_MS) #make this customizable
    

def reset():
    random_numbers = [random.randint(1, MAX_VALUE) for _ in range(DATA_SIZE)]
    global plotting
    plotting = False
    global comparisons 
    comparisons = 0

def create_textbox(title: str, colour: pygame.Color, x: int, y: int, font: pygame.font.Font): #add font
    # Create a font object
    text_surface  = font.render(title, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    return text_surface, text_rect

class DropDownBox():
    
    def __init__(self, x, y, w, h, colour, highlight_colour, font, default, options, selected = -1):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour
        self.highlight_colour = highlight_colour
        self.font = font
        self.default = default
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.selected = selected

    def draw(self, surface):
        #pygame.draw.rect(surface, purpleBlock, self.rect) # boxframe
        default_surface, default_rect = create_textbox(self.default, purpleBlock, self.rect.center[0], self.rect.center[1], self.font)
        screen.blit(default_surface, default_rect)

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.h
                option_surface, option_rect = create_textbox(text, purpleBlock, rect.center[0], rect.center[1], dropDownFont)
                screen.blit(option_surface, option_rect)
                #draw each option and display

    def update(self, event_list):
        mousePos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mousePos)
        self.selected = -1 #reset to nothing selected for next update

        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.h
            if rect.collidepoint(mousePos):
                self.selected = i
                break #can only select one thing at a time so don't needa check the rest

        if not self.menu_active and self.selected == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Case to expand and minimise
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                #Case to return selected option
                elif self.draw_menu and self.selected >= 0:
                    self.draw_menu = False
                    return self.selected
        return -1

# Generate a list of random numbers
DATA_SIZE = 50 #make this customizable & keep them even to prevent rounding errors when drawing & positioning
MAX_VALUE = 800 #Anything greater than screen_height would go over the frame...

#Pygame setup
ALGORITHMS = ["bubble sort", "insertion sort", "selection sort", "quick sort"]
DELAY_IN_MS = 1
UI_WIDTH_PADDING = 50
UI_HEIGHT_PADDING = 200
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

pygame.init()
pygame.display.set_caption("Sorting Algorithm Visualizer")
screen = pygame.display.set_mode((SCREEN_WIDTH + UI_WIDTH_PADDING , SCREEN_HEIGHT + UI_HEIGHT_PADDING))
clock = pygame.time.Clock()

titleFont = pygame.font.Font(None, 36)  # You can specify a font file or use None for a default font
dropDownFont = pygame.font.Font(None, 20)  # You can specify a font file or use None for a default font
purpleBlock =  pygame.Color(67, 1, 135, 255)

dropDownBox = DropDownBox(20/2 + 25, SCREEN_HEIGHT + UI_HEIGHT_PADDING/2, 100, 20, purpleBlock, purpleBlock, dropDownFont, "Algorithms", ALGORITHMS, -1)

running = True
plotting = False
comparisons  = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        #Event for loading iterator comes here, then we draw
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    # RENDER YOUR GAME HERE
    dropDownBox.draw(screen)
    dropDownBox.selected  = dropDownBox.update(event_list)
    print(dropDownBox.selected)
    #if (dropDownBox.selected != -1):
    #    print(f"{dropDownBox.options[dropDownBox.selected]}")
    if plotting:
        try:
            update_plot(next(data_iterator), titleText) #Raises StopIteration error on completion
        except StopIteration:
            print("The data has been sorted")
            reset()
        except Exception as e:
            print(f"An unexpected exception occurred: {e}")
        else:
            print("Nothing to plot.")
    else:
        if (dropDownBox.selected != -1):
            random_numbers = [random.randint(1, MAX_VALUE) for _ in range(DATA_SIZE)]
            print(f"{random_numbers}")
            titleText = dropDownBox.options[dropDownBox.selected]
            plotting = True
            if (dropDownBox.options[dropDownBox.selected] == "bubble sort"):
                data_iterator = bubblesort(random_numbers)
            elif (dropDownBox.options[dropDownBox.selected] == "insertion sort"):
                data_iterator = insertion_sort(random_numbers)
            elif (dropDownBox.options[dropDownBox.selected] == "selection sort"):
                data_iterator = selection_sort(random_numbers)
            elif (dropDownBox.options[dropDownBox.selected] == "quick sort"):
                data_iterator = quicksort(random_numbers, 0, DATA_SIZE - 1)
                #print(f"Data iterator: {list(data_iterator)}")
    
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()


