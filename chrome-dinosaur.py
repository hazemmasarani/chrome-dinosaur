import pygame
import sys
from math import ceil
from random import randint

import pygame.locals

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 30
GAME_SPEED = 27
MAX_SPEED = 30
MIN_SPEED = 1
BACKGROUND_COLOR = (135,206,235)

pygame.display.set_caption('Chrome Dinosaur🦖')
clock = pygame.time.Clock()

# create objects
class Dinosaur:
    running_frames = None
    jump_frames = None
    walk_frames = None
    duck_frames = None

    def __init__(self, pos_x, pos_y, width, height):
        # Load sprite frames only once
        if not Dinosaur.running_frames:
            Dinosaur.running_frames = []
            for i in range(1, 9):
                img = pygame.image.load(f'assets\\sprite\\dinosaur\\running\\Run ({i}).png').convert_alpha()
                Dinosaur.running_frames.append(pygame.transform.scale(img, (width, height)))

        if not Dinosaur.jump_frames:
            Dinosaur.jump_frames = []
            for i in range(1, 13):
                img = pygame.image.load(f'assets\\sprite\\dinosaur\\jumping\\Jump ({i}).png').convert_alpha()
                Dinosaur.jump_frames.append(pygame.transform.scale(img, (width, height)))

        if not Dinosaur.walk_frames:
            Dinosaur.walk_frames = []
            for i in range(1, 11):
                img = pygame.image.load(f'assets\\sprite\\dinosaur\\walking\\Walk ({i}).png').convert_alpha()
                Dinosaur.walk_frames.append(pygame.transform.scale(img, (width, height)))

        if not Dinosaur.duck_frames:
            Dinosaur.duck_frames = []
            for i in range(1, 5):
                img = pygame.image.load(f'assets\\sprite\\dinosaur\\ducking\\Duck ({i}).png').convert_alpha()
                Dinosaur.duck_frames.append(pygame.transform.scale(img, (width, height)))

        self.step_index = 0
        self.pos_x, self.pos_y = pos_x, pos_y
        self.first_pos_x, self.first_pos_y = pos_x, pos_y
        self.cur_running_frame_indx = 0
        self.cur_jumping_frame_indx = 0
        self.cur_ducking_frame_indx = 0
        self.state = "running"  # Default state is running
        self.JUMP_VEL = self.jump_vel= 6
        self.dv = 0.43

    def update(self, key_pressed=None, key_released = None):
        # Update frames based on user input
        if self.step_index >= FPS:
            self.step_index = 0
        
        if self.state == "running":
            self.run()
            if key_pressed and key_pressed == "up":
                self.state = "jumping"
                self.cur_jumping_frame_indx = 0
            elif key_pressed and key_pressed == "down":
                self.state = "ducking"
                self.cur_ducking_frame_indx = 0
        elif self.state == "jumping":
            self.jump()
            if self.pos_y >= self.first_pos_y:
                self.state = "running"
                self.pos_x, self.pos_y = self.first_pos_x, self.first_pos_y
                self.jump_vel = self.JUMP_VEL
                self.cur_running_frame_indx = 0
        elif self.state == "ducking":
            self.duck()
        else:
            self.run()
            self.state = "running"
        if key_released == "down":
            self.state = "running"

    def run(self):
        running_frames_count = len(Dinosaur.running_frames)
        sprite_speed = MAX_SPEED - GAME_SPEED
        if sprite_speed < MIN_SPEED:
            sprite_speed = MIN_SPEED
        if self.step_index % sprite_speed == 0:
            self.cur_running_frame_indx += 1
            self.cur_running_frame_indx %= running_frames_count
        self.step_index += 1
    
    def jump(self):
        jump_frames_count = len(Dinosaur.jump_frames)
        sprite_speed = MAX_SPEED - GAME_SPEED
        if sprite_speed < MIN_SPEED:
            sprite_speed = MIN_SPEED
        if self.step_index % sprite_speed == 0:
            self.cur_jumping_frame_indx += 1
            self.cur_jumping_frame_indx %= jump_frames_count
        self.step_index += 1
        if self.jump_vel > 0:
            self.pos_y -= self.jump_vel * self.jump_vel
        else:
            self.pos_y += self.jump_vel * self.jump_vel
        self.jump_vel -= self.dv

    def duck(self):
        duck_frames_count = len(Dinosaur.duck_frames)
        sprite_speed = MAX_SPEED - GAME_SPEED
        if sprite_speed < MIN_SPEED:
            sprite_speed = MIN_SPEED
        if self.step_index % sprite_speed == 0:
            self.cur_ducking_frame_indx += 1
            self.cur_ducking_frame_indx %= duck_frames_count
        self.step_index += 1

    def draw(self):
        if self.state == "running":
            SCREEN.blit(Dinosaur.running_frames[self.cur_running_frame_indx], (self.pos_x, self.pos_y))
        elif self.state == "jumping":
            SCREEN.blit(Dinosaur.jump_frames[self.cur_jumping_frame_indx], (self.pos_x, self.pos_y))
        elif self.state == "ducking":
            SCREEN.blit(Dinosaur.duck_frames[self.cur_ducking_frame_indx], (self.pos_x, self.pos_y))

class Ground:

    surface_tile = None
    buttom_tile = None

    def __init__(self):
        if not Ground.surface_tile:
            ground_tiles = pygame.image.load(f'assets\\background\\pr.png').convert_alpha()
            Ground.surface_tile = ground_tiles.subsurface(pygame.Rect(185, 19, 75, 75))
        if not Ground.buttom_tile:
            ground_tiles = pygame.image.load(f'assets\\background\\pr.png').convert_alpha()
            Ground.buttom_tile = ground_tiles.subsurface(pygame.Rect(185, 103, 75, 75))
        self.surface = []
        for i in range(0, SCREEN_WIDTH + 75 * 2, 75):
            self.surface.append([i, SCREEN_HEIGHT//2])
        self.buttom = []
        for j in range(SCREEN_HEIGHT//2 + 75, SCREEN_HEIGHT + 75 * 2, 75):
            self.buttom.append([])
            for i in range(0, SCREEN_WIDTH + 75 * 2, 75):
                self.buttom[-1].append([i, j])

    def update(self):
        if self.surface[0][0] < -75:
            self.surface[0][0] = self.surface[-1][0] + 75
            self.surface.append(self.surface[0])
            del self.surface[0]
        else:
            for tile in self.surface:
                tile[0] -= GAME_SPEED//3
        
        for row in self.buttom:
            if row[0][0] <= -75:
                row[0][0] = row[-1][0] + 75
                row.append(row[0])
                del row[0]
        else:
            for row in self.buttom:
                for tile in row:
                    tile[0] -= GAME_SPEED//3

    def draw(self):
        for [x,y] in self.surface:
            SCREEN.blit(Ground.surface_tile,(x,y))
        for row in self.buttom:
            for [x,y] in row:
                SCREEN.blit(Ground.buttom_tile,(x,y))

class Cactus:

    cactus_frames = None

    def __init__(self, index):
        cuts = [0, 85, 150, 185]  # X-coordinates for the cuts
        sizes = [(85, 80), (65, 60), (35, 60), (25, 40)]  # (width, height) of each frame
        # Initialize cactus frames only if not already initialized
        if not Cactus.cactus_frames:
            cactus_image = pygame.image.load(f'assets\\sprite\\cactus\\cactus.png').convert_alpha()
            Cactus.cactus_frames = []
            
            # Loop to create each subsurface from the sprite sheet
            for i in range(len(cuts)):
                Cactus.cactus_frames.append(cactus_image.subsurface(pygame.Rect(cuts[i], 80 - sizes[i][1], sizes[i][0], sizes[i][1])))

        # Assign the cactus frame, optionally resizing it
        self.cactus_frame = Cactus.cactus_frames[index]

        # Assign position using sizes for alignment
        self.pos_x, self.pos_y = SCREEN_WIDTH + 200, SCREEN_HEIGHT // 2 - sizes[index][1]

    def update(self):
        self.pos_x -= GAME_SPEED//3

    def draw(self):
        SCREEN.blit(self.cactus_frame,(self.pos_x,self.pos_y))

# Sprites
dino = Dinosaur(SCREEN_WIDTH//10, SCREEN_HEIGHT//2 - 90, 150, 100)
ground = Ground()
obsticals = []
obstical_cntr = 0
obstical_thr = 100
key_pressed = None
key_released = None
running = True

while running:

    x, y = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(e.key)
        if e.type == pygame.KEYUP:
            if pygame.key.name(e.key) == key_pressed:
                key_pressed = None
            key_released = pygame.key.name(e.key)

    if not running:
        break

    obstical_cntr += 1
    # if obstical_cntr == 2:
    #     break
    if obstical_cntr % obstical_thr == 0:
        obsticals.append(Cactus(randint(0, 3)))

    SCREEN.fill(BACKGROUND_COLOR)
    dino.update(key_pressed, key_released)
    ground.update()

    to_be_removed_from_obsticals = []

    for indx, obstical in enumerate(obsticals):
        if obstical.pos_x < -100:
            to_be_removed_from_obsticals.append(indx)
        obstical.update()

    # Remove obstacles from the list after iteration
    # To avoid index shift problems, we should iterate in reverse order
    for indx in reversed(to_be_removed_from_obsticals):
        del obsticals[indx]

    ground.draw()
    dino.draw()

    for obstical in obsticals:
        obstical.draw()

    key_released = None
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
sys.exit()