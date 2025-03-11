import pygame
import sys
from random import randint
from math import pow, sqrt

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT - SCREEN_HEIGHT // 3
FPS = 30
GAME_SPEED = 15
BACKGROUND_COLOR = (135, 206, 235)

pygame.display.set_caption('Chrome Dinosaur🦖')
clock = pygame.time.Clock()

# Dinosaur Class
class Dinosaur:

    def __init__(self, pos_x, width, height):
        self.pos_x, self.pos_y = pos_x, GROUND_Y - height
        self.width, self.height = width, height
        self.is_jumping = False
        self.gravity = 0.02
        self.cur_velocity = self.initial_velocity = 15
        self.jump_time = 0
        
    def run(self):
        return 

    def jump(self):
        self.cur_velocity -= self.gravity * self.jump_time
        self.jump_time += 2
        self.pos_y -= int(self.cur_velocity)
        if self.pos_y > GROUND_Y - self.height:
            self.is_jumping = False
            self.cur_velocity = self.initial_velocity
            self.jump_time = 0
            self.pos_y = GROUND_Y - self.height

    def update(self, key_pressed):

        if self.is_jumping:
            self.jump()
        elif key_pressed == "up":
            self.is_jumping = True
        else:
            self.run()

    def draw(self):
        pygame.draw.rect(SCREEN, (0, 255, 0), (self.pos_x, self.pos_y, self.width, self.height))

# Ground Class
class Ground:
    ground_tile = None

    def __init__(self):
        if not Ground.ground_tile:
            Ground.ground_tile = pygame.image.load(f'assets\\background\\ground_tile.png').convert_alpha()
        self.width = Ground.ground_tile.get_width()
        self.tiles_coor = [[0, GROUND_Y], [self.width, GROUND_Y]]

    def update(self):
        for tile_coor in self.tiles_coor:
            tile_coor[0] -= GAME_SPEED
        if self.tiles_coor[0][0] < -self.width:
            self.tiles_coor[0][0] = self.tiles_coor[1][0] + self.width
            self.tiles_coor[0], self.tiles_coor[1] = self.tiles_coor[1], self.tiles_coor[0]

    def draw(self):
        for [x, y] in self.tiles_coor:
            SCREEN.blit(Ground.ground_tile,(x,y))

# Cactus Class
class Cactus:
    def __init__(self, x_pos):
        self.width, self.height = 40, 60
        self.x_pos = x_pos
        self.y_pos = SCREEN_HEIGHT - 100 - self.height

    def update(self):
        self.x_pos -= GAME_SPEED 

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 0, 0), (self.x_pos, self.y_pos, self.width, self.height))

# Game Initialization
dino = Dinosaur(100, 50, 100)
ground = Ground()
cacti = []

running = True
key_pressed = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key)
        if event.type == pygame.KEYUP:
            key_pressed = None

    # Update game state
    SCREEN.fill(BACKGROUND_COLOR)
    dino.update(key_pressed)
    ground.update()

    # Update obstacles (Cacti)
    if randint(0, 100) < 2:  # Randomly spawn cactus
        cacti.append(Cactus(SCREEN_WIDTH))

    to_remove = []
    for cactus in cacti:
        cactus.update()
        if cactus.x_pos < -cactus.width:
            to_remove.append(cactus)

    # Remove obstacles off-screen
    for cactus in to_remove:
        cacti.remove(cactus)

    # Draw everything
    ground.draw()
    dino.update(key_pressed)
    dino.draw()

    for cactus in cacti:
        cactus.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()