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


    def setPath(self):
        self.color = COLORS['TURQUOISE']

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
        self.neighbors = []
        if self.row < self.rows - 1 and not grid[self.row + 1][self.column].isObstacle():
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].isObstacle():
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < self.rows - 1 and not grid[self.row][self.column + 1].isObstacle():
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].isObstacle():
            self.neighbors.append(grid[self.row][self.column - 1])

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

    row = x // gap
    column = y // gap

    return row, column


def reconstruct_path(previousPath, current, draw):
    while current in previousPath:
        current.setPath()
        current = previousPath[current]
        draw()


def algorithm(draw, grid, startPosition, endPosition):
    counter = 0
    nodeQueue = PriorityQueue()
    nodeQueue.put((0, counter, startPosition))  # nodul de inceput
    previousPath = {}
    g_function = {spot: float("inf") for row in grid for spot in row}
    g_function[startPosition] = 0
    f_function = {spot: float("inf") for row in grid for spot in row}
    f_function[startPosition] = hFunction(startPosition.getPosition(), endPosition.getPosition())

    setHash = {startPosition}  # tine minte cine e in nodeQueue

    while not nodeQueue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = nodeQueue.get()[2]  # ia elementul de pe poz 2, adica nodul la care ne aflam, nodul curent
        setHash.remove(current)

        if current == endPosition:
            reconstruct_path(previousPath, endPosition, draw)
            break

        for neighbor in current.neighbors:
            g_score_temporar = g_function[current] + 1

            if g_score_temporar < g_function[neighbor]:
                previousPath[neighbor] = current
                g_function[neighbor] = g_score_temporar
                f_function[neighbor] = g_score_temporar + hFunction(neighbor.getPosition(), endPosition.getPosition())
                if neighbor not in setHash:
                    counter += 1
                    nodeQueue.put((f_function[neighbor], counter, neighbor))
                    setHash.add(neighbor)
                    neighbor.setNotVisited()
            draw()

            if current != startPosition:
                current.setVisited()
    return False


def main(window, width):
    rows = 50
    grid = build_grid(rows, width)

    startPosition = None
    endPosition = None

    run = True

    draw(window, grid, rows, width)
    while run:
        draw(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = getPositionByMouse(position, rows, width)
                square = grid[row][column]
                if not startPosition and square != startPosition:
                    startPosition = square
                    startPosition.setStart()
                elif not endPosition and square != startPosition:
                    endPosition = square
                    endPosition.setEnd()

                elif square != startPosition and square != endPosition:
                    square.setObstacle()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = getPositionByMouse(position, rows, width)
                square = grid[row][column]
                square.reset()
                if square == startPosition:
                    startPosition = None
                elif square == endPosition:
                    endPosition = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startPosition and endPosition:
                    for row in grid:
                        for column in row:
                            column.update_neighbors(grid)
                    algorithm(lambda: draw(window, grid, rows, width), grid, startPosition, endPosition)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = build_grid(rows, width)
    pygame.quit()


main(window, width)
