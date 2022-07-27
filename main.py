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


class Square:
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

    def setStart(self):
        self.color = COLORS['ORANGE']

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

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False


def hFunction(h1, h2):
    x1, y1 = h1
    x2, y2 = h2
    return abs(x1 - x2) + abs(y1 - y2)

def build_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)

    return grid

def build_grid_lines(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, COLORS['GREY'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, COLORS['GREY'], (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
    window.fill(COLORS['WHITE'])
    for row in grid:
        for square in row:
            square.draw(window)

    build_grid_lines(window, rows, width)
    pygame.display.update()

def getPositionByMouse(position, rows, width):
    gap = width // rows
    x, y = position

    row = y // gap
    column = x // gap

    return row, column


def main(window, width):
    rows = 50
    grid = build_grid(rows, width)

    startPosition = None
    endPosition = None

    run = True
    started = True

    draw(window, grid, rows, width)
    while run:
        draw(window, grid, rows, width)
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                print("merge")
                position = pygame.mouse.get_pos()
                row, column = getPositionByMouse(position, rows, width)
                square = grid[row][column]
                if not startPosition:
                    startPosition = square
                    startPosition.setStart()
                    print(3)
                elif not endPosition:
                    endPosition = square
                    endPosition.setEnd()
                    print(3)

                elif square != startPosition and square != endPosition:
                    square.setObstacle()

            elif pygame.mouse.get_pressed()[2]:
                pass

    pygame.quit()


main(window, width)
