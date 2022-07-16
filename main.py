import pygame
import math
from queue import PriorityQueue

COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 255, 0),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'GREY': (128, 128, 128),
    'TURQUOISE': (64, 224, 208)
}

width = 800
window = pygame.display.set_mode((width, width))


class Cube:
    def __init__(self, row, column, width, rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = COLORS['WHITE']
        self.neighbors = []
        self.width = width
        self.rows = rows

    def getPosition(self):
        return self.row, self.column

    def isVisited(self):
        return self.color == COLORS['RED']

    def isNotVisited(self):
        return self.color == COLORS['GREEN']

    def isObstacle(self):
        return self.color == COLORS['BLACK']

    def isStart(self):
        return self.color == COLORS['ORANGE']

    def isEnd(self):
        return self.color == COLORS['PURPLE']

    def reset(self):
        self.color = COLORS['WHITE']

    def setVisited(self):
        self.color = COLORS['RED']

    def setNotVisited(self):
        self.color = COLORS['GREEN']

    def setObstacle(self):
        self.color = COLORS['BLACK']

    def setStart(self):
        self.color = COLORS['ORANGE']

    def setEnd(self):
        self.color = COLORS['PURPLE']