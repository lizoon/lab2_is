import pygame
import math
from board import boards

pygame.init()

# game init
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
PI = math.pi

# player motion
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/images/pacman/{i}.png'), (45, 45)))

# starting position
player_x = 450
player_y = 663
direction = 0
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    num3 = 15
    # check collisions based on center x and center y of player +/- fadge factor
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + num3) // num1][center_x // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - num3) // num1][center_x // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed


