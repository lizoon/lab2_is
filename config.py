import pygame
import copy
from board import boards

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
level = copy.deepcopy(boards)

