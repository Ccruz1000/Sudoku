import pygame
import sys
from settings import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = test_board
        self.selected = None
        self.mousepos = None
        self.state = "playing"

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None

    def playing_update(self):
        self.mousepos = pygame.mouse.get_pos()

    def playing_draw(self):
        self.window.fill(WHITE)
        if self.selected:
            self.draw_selection(self.window, self.selected)
        self.drawgrid(self.window)
        pygame.display.update()

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
