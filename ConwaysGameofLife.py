import pygame, sys, math, copy
from pygame.locals import *

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
SCALE = 10

BLACK = (0,0,0)
DARKER_GREY = (50,50,50)
DARK_GREY = (100,100,100)
GREY = (128,128,128)
LIGHT_GREY = (180,180,180)
WHITE = (255,255,255)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
pygame.display.set_caption("Conway's Game of Life")

class Button:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        self.hover = False
    
    def checkClick(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
    def draw(self):
        if self.hover:
            pygame.draw.rect(screen, DARK_GREY, self.rect)
        else:
            pygame.draw.rect(screen, LIGHT_GREY, self.rect)
        renderText(self.name, 40, BLACK, self.rect)

def update(grid):
    newGrid = [[0 for j in range(SCREEN_WIDTH // SCALE + 4)] for i in range(SCREEN_HEIGHT // SCALE + 4)]
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            live = getNeighbours(grid, row, column).count(1)
            
            if grid[row][column] == 1:
                if (live < 2 or live > 3):
                    newGrid[row][column] = 0
                else:
                    newGrid[row][column] = 1
                
            elif grid[row][column] == 0 and (live == 3):
                newGrid[row][column] = 1
                
    return newGrid
                
def getNeighbours(grid, row, column):
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                try:
                    neighbours.append(grid[row+i][column+j])
                except:
                    neighbours.append(0)
    return neighbours

def drawGrid(grid):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 0:
                pygame.draw.rect(screen, BLACK, pygame.Rect((column-2) * SCALE + 1, (row-2) * SCALE + 1, SCALE - 1, SCALE - 1))
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect((column-2) * SCALE + 1, (row-2) * SCALE + 1, SCALE - 1, SCALE - 1))

def drawUI(generations, population, running, buttons, mousePos):
    screen.blit(pygame.font.SysFont("Consolas", 30).render(f"Generations: {generations}", False, WHITE), (5,5))
    screen.blit(pygame.font.SysFont("Consolas", 30).render(f"Population: {population}", False, WHITE), (5,55))
    
    for button in buttons:
        if button.checkClick(mousePos):
            button.hover = True
        else:
            button.hover = False
        button.draw()

def renderText(text, size, colour, rect):
    font = pygame.font.SysFont("Consolas", size)
    textSize = font.size(text)
    screen.blit(font.render(text, False, colour), (rect.centerx - textSize[0]/2, rect.centery - textSize[1]/2))

grid = [[0 for j in range(SCREEN_WIDTH // SCALE + 4)] for i in range(SCREEN_HEIGHT // SCALE + 4)]
buttons = [Button("Start", pygame.Rect(200, SCREEN_HEIGHT - 75, 150, 50)),
           Button("Reset", pygame.Rect(20, SCREEN_HEIGHT - 75, 150, 50))]

population = 0
generations = 0
running = False
drawing = False
erasing = False

while True:
    clock.tick(60)
    screen.fill(DARKER_GREY)
    pressedKeys = pygame.key.get_pressed()
    mousePos = pygame.Vector2(pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            erasing = False
            drawing = False
            for button in buttons:
                if button.checkClick(mousePos):
                    if button.name == "Start":
                        running = True
                        button.name = "Stop"
                    elif button.name == "Stop":
                        running = False
                        button.name = "Start"
                    elif button.name == "Reset":
                        grid = [[0 for j in range(SCREEN_WIDTH // SCALE + 4)] for i in range(SCREEN_HEIGHT // SCALE + 4)]
                        population = 0
                        generations = 0
                        running = False
                        buttons[0].name = "Start"
                        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not running:
                if event.button == 1:
                    drawing = True
                elif event.button == 3:
                    erasing = True

    if (drawing or erasing) and not running:
        gridPos = mousePos // SCALE
        try:
            if drawing:
                if grid[int(gridPos[1])+2][int(gridPos[0])+2] == 0:
                    grid[int(gridPos[1])+2][int(gridPos[0])+2] = 1
                    population += 1
            elif erasing:
                if grid[int(gridPos[1])+2][int(gridPos[0])+2] == 1:
                    grid[int(gridPos[1])+2][int(gridPos[0])+2] = 0
                    population -= 1
        except:
            pass
    
    if running:
        grid = update(grid)
        population = [cell for row in grid for cell in row].count(1)
        generations += 1
        
    drawGrid(grid)
    drawUI(generations, population, running, buttons, mousePos)
    
    pygame.display.update()