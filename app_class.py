import pygame
import sys
from settings import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = test_board

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.window.fill(WHITE)
        self.drawgrid(self.window)
        pygame.display.update()

    def drawgrid(self, window):
        pygame.draw.rect(window, BLACK, (grid_pos[0], grid_pos[1], WIDTH-2 * out_buff, HEIGHT-2 * out_buff), 2)
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


            pass