import pygame
import sys
from settings import *
from button_class import *
import numpy as np
from dokusan import generators
from solver import *
import random
import copy

# Init Board
board = [[0 for x in range(9)] for x in range(9)]


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = board
        self.selected = None
        self.mousepos = None
        self.state = "playing"
        self.finished = False
        self.cell_changed = False
        self.playing_buttons = []
        self.locked_cells = []
        self.incorrect_cells = []
        self.font = pygame.font.SysFont("arial", int(cell_size//2))
        self.load()

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

# Playing State Function

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # User Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playing_buttons:
                        if button.highlighted:
                            button.click()
            # User types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.locked_cells:
                    if self.is_int(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cell_changed = True

    def playing_update(self):
        self.mousepos = pygame.mouse.get_pos()
        for button in self.playing_buttons:
            button.update(self.mousepos)

        if self.cell_changed:
            self.incorrect_cells = []
            if self.all_cells_done():
                # Check if board is correct
                self.check_all_cells()
                if len(self.incorrect_cells) == 0:
                    self.finished = True
                    button.draw(self.window)
                    self.playing_draw()
                    self.load()

    def playing_draw(self):
        self.window.fill(WHITE)
        if self.selected:
            self.draw_selection(self.window, self.selected)
        self.shade_locked_cells(self.window, self.locked_cells)
        self.shade_incorrect_cells(self.window, self.incorrect_cells)
        self.draw_numbers(self.window)
        self.drawgrid(self.window)
        for button in self.playing_buttons:
            button.draw(self.window)
        pygame.display.update()
        self.cell_changed = False

# Board Checking Functions

    def all_cells_done(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True

    def check_all_cells(self):
        self.check_rows()
        self.check_cols()
        self.check_small_grid()

    def check_rows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for i in range(9):
                            if self.grid[yidx][i] == self.grid[yidx][xidx] and [i, yidx] not in self.locked_cells:
                                self.incorrect_cells.append([i, yidx])

    def check_cols(self):
        for xidx in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for i , row in enumerate(self.grid):
                            if self.grid[i][xidx] == self.grid[yidx][xidx] and [xidx, i] not in self.locked_cells:
                                self.incorrect_cells.append([xidx, i])

    def check_small_grid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(3):
                    for j in range(3):
                        xidx = x*3 + i
                        yidx = y*3 + j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                                self.incorrect_cells.append([xidx, yidx])
                            if [xidx, yidx] in self.locked_cells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3 + k
                                        yidx2 = y*3 + l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.locked_cells:
                                            self.incorrect_cells.append([xidx2, yidx2])

# Helper Functions

    def get_puzzle(self, difficulty):
        if difficulty == 1:
            board = [[0 for x in range(9)] for x in range(9)]
        else:
            board = np.array(list(str(generators.random_sudoku(avg_rank=difficulty))))
            board = board.astype(int)
            board = board.reshape((9, 9))
            board = board.tolist()
        self.grid = board
        self.load()

    def solve_puzzle(self, bo):
        solve(bo)

    def hint(self):
        placeholder = copy.deepcopy(self.grid)
        solved_board = solve(placeholder)
        cntr = 0
        while cntr < 3:
            xidx = random.randint(0, 8)
            yidx = random.randint(0, 8)
            if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                self.grid[yidx][xidx] = solved_board[yidx][xidx]
                cntr += 1
        self.load()

    def draw_numbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [(xidx * cell_size) + grid_pos[0], (yidx * cell_size) + grid_pos[1]]
                    self.text_to_screen(window, str(num), pos)

    def draw_selection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE, ((pos[0]*cell_size)+grid_pos[0], (pos[1]*cell_size)+grid_pos[1],
                                             cell_size, cell_size))

    def drawgrid(self, window):
        pygame.draw.rect(window, BLACK, (grid_pos[0], grid_pos[1], WIDTH-(2 * out_buff), HEIGHT-(2 * out_buff)), 2)
        for x in range(9):
            if x % 3 != 0:
                pygame.draw.line(window, BLACK, (grid_pos[0] + (x * cell_size), grid_pos[1]),
                                 (grid_pos[0] + (x * cell_size), grid_pos[1] + 450))
                pygame.draw.line(window, BLACK, (grid_pos[0], grid_pos[1] + (x * cell_size)),
                                 (grid_pos[0] + 450, grid_pos[1] + (x * cell_size)))
            else:
                pygame.draw.line(window, BLACK, (grid_pos[0] + (x * cell_size), grid_pos[1]),
                                 (grid_pos[0] + (x * cell_size), grid_pos[1] + 450), 3)
                pygame.draw.line(window, BLACK, (grid_pos[0], grid_pos[1] + (x * cell_size)),
                                 (grid_pos[0] + 450, grid_pos[1] + (x * cell_size)), 3)

    def mouse_on_grid(self):
        if self.mousepos[0] < grid_pos[0] or self.mousepos[1] < grid_pos[1]:
            return False
        if self.mousepos[0] > grid_pos[0] + grid_size or self.mousepos[1] > grid_pos[1] + grid_size:
            return False
        return (self.mousepos[0] - grid_pos[0])//cell_size, (self.mousepos[1] - grid_pos[1])//cell_size

    def load_buttons(self):
        # Check
        self.playing_buttons.append(Button(500, 50, WIDTH//7, 40,
                                           function=self.check_all_cells,
                                           color=(27, 142, 207), text='Check'))
        # Submit
        self.playing_buttons.append(Button(380, 50, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(117, 172, 112), text='Submit', params=1))
        # Beginner
        self.playing_buttons.append(Button(20, 0, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(15, 255, 51), text='Beginner', params=50))
        # Easy
        self.playing_buttons.append(Button(20, 50, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(255, 247, 15), text='Easy', params=150))
        # Medium
        self.playing_buttons.append(Button(140, 0, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(255, 147, 15), text='Medium', params=225))
        # Hard
        self.playing_buttons.append(Button(140, 50, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(255, 0, 75), text='Hard', params=300))
        # Very Hard
        self.playing_buttons.append(Button(WIDTH // 2 - (WIDTH//7) // 2, 0, WIDTH // 7, 40,
                                           function=self.get_puzzle,
                                           color=(255, 0, 0), text='Very Hard', params=400))
        # Load
        self.playing_buttons.append(Button(380, 0, WIDTH // 7, 40,
                                           function=self.load,
                                           color=(153, 153, 255), text='Load'))
        # Solve
        self.playing_buttons.append(Button(500, 0, WIDTH // 7, 40, function=self.solve_puzzle,
                                           color=(0, 255, 247), text='Solve', params=self.grid))
        # Hint
        self.playing_buttons.append(Button(WIDTH // 2 - (WIDTH//7) // 2, 50, WIDTH // 7, 40, function=self.hint,
                                                   color=(195, 0, 255), text='Hint'))
        if len(self.incorrect_cells) == 0 and self.finished is True:
            self.playing_buttons.append(Button(200, 275, 200, 100, color=(3, 11, 252), highlightcolor=(3, 11, 252),
                                               text='Congratulations'))

    def text_to_screen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        font_width = font.get_width()
        font_height = font.get_height()
        pos[0] += (cell_size - font_width)//2
        pos[1] += (cell_size - font_height)//2
        window.blit(font, pos)

    def shade_locked_cells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOR, ((cell[0] * cell_size) + grid_pos[0], (cell[1] * cell_size)
                                                       + grid_pos[1], cell_size, cell_size))

    def shade_incorrect_cells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLCOLOR, ((cell[0] * cell_size) + grid_pos[0], (cell[1] * cell_size)
                                                       + grid_pos[1], cell_size, cell_size))

    def load(self):
        self.playing_buttons = []
        self.load_buttons()
        self.locked_cells = []
        self.finished = False
        self.incorrect_cells = []
        # Setting locked cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.locked_cells.append([xidx, yidx])

    def is_int(self, string):
        try:
            int(string)
            return True
        except:
            return False

# TODO Add option to pencil in possible values
