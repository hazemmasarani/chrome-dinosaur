import pygame
import sys
import os
from random import randint

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT - SCREEN_HEIGHT // 3
FPS = 30
GAME_SPEED = 25
BACKGROUND_COLOR = (135, 206, 235)
JX = GAME_SPEED * 5
RX = GAME_SPEED * 20
MIN_OBS_H = 60
MAX_OBS_H = 120
MAX_NUM_OBS_PER_CHUNCK = 6

pygame.display.set_caption('Chrome Dinosaur🦖')
clock = pygame.time.Clock()

# Dinosaur Class
class Dinosaur:

    running_frames = None
    jumping_frames = None

    def __init__(self, pos_x, height):
        self.height = height
        if not Dinosaur.running_frames:
            Dinosaur.running_frames = []
            for path in os.listdir('assets\\sprite\\dinosaur\\running\\'):
                frame = pygame.image.load(f'assets\\sprite\\dinosaur\\running\\{path}').convert_alpha()
                self.width = frame.get_width() * height // frame.get_height()
                scaled_frame = pygame.transform.scale(frame, (self.width, self.height))
                Dinosaur.running_frames.append(scaled_frame)
        if not Dinosaur.jumping_frames:
            Dinosaur.jumping_frames = []
            for path in os.listdir('assets\\sprite\\dinosaur\\jumping\\'):
                frame = pygame.image.load(f'assets\\sprite\\dinosaur\\jumping\\{path}').convert_alpha()
                self.width = frame.get_width() * height // frame.get_height()
                scaled_frame = pygame.transform.scale(frame, (self.width, self.height))
                Dinosaur.jumping_frames.append(scaled_frame)
        self.cur_frame = None
        self.width = Dinosaur.running_frames[0].get_width()
        self.height -= 10
        self.pos_x, self.pos_y = pos_x, GROUND_Y - self.height
        self.is_jumping = False
        self.gravity = 0.02
        self.cur_velocity = self.initial_velocity = 15
        self.jump_time = 0
        self.jump_frame_index = 0
        self.running_frame_index = 0

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
        if GAME_SPEED == 0: 
            return
        
        if self.is_jumping:
            self.jump()
        elif key_pressed == "up":
            self.is_jumping = True
        else:
            self.run()

    def draw(self):
        if self.is_jumping:
            SCREEN.blit(Dinosaur.jumping_frames[self.jump_frame_index // 2],(self.pos_x, self.pos_y))
            self.cur_frame = Dinosaur.jumping_frames[self.jump_frame_index // 2]
            if GAME_SPEED != 0:
                self.jump_frame_index += 1
                self.jump_frame_index %= len(Dinosaur.jumping_frames)*2
                self.running_frame_index = 0
        else:
            SCREEN.blit(Dinosaur.running_frames[self.running_frame_index // 3],(self.pos_x, self.pos_y))
            self.cur_frame = Dinosaur.running_frames[self.running_frame_index // 3]
            if GAME_SPEED != 0:
                self.running_frame_index += 1
                self.running_frame_index %= len(Dinosaur.running_frames)*3
                self.jump_frame_index = 0

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
    cactus_images = None
    def __init__(self, pos_x, height):
        if not Cactus.cactus_images:
            Cactus.cactus_images = []
            for i in range(2):
                Cactus.cactus_images.append(pygame.image.load(f'assets\\sprite\\cactus\\cactus ({i}).png').convert_alpha())
        cactus_index = randint(0,1)
        self.height = height
        self.width = Cactus.cactus_images[cactus_index].get_width() * self.height // Cactus.cactus_images[cactus_index].get_height()
        self.cur_frame = pygame.transform.scale(Cactus.cactus_images[cactus_index], (self.width, self.height))
        self.pos_x = pos_x
        self.pos_y = GROUND_Y - self.height

    def update(self):
        self.pos_x -= GAME_SPEED

    def draw(self):
        SCREEN.blit(self.cur_frame,(self.pos_x, self.pos_y))

class Obstical:

    def __init__(self):
        self.l_jx = SCREEN_WIDTH
        
    def update(self):
        self.l_jx -= GAME_SPEED
        if self.l_jx <= SCREEN_WIDTH - RX:
            self.l_jx = SCREEN_WIDTH + JX
            self.generate_cacti(SCREEN_WIDTH, SCREEN_WIDTH + JX)

    def generate_cacti(self,lim_x1, lim_x2):
        for i in range(randint(0, MAX_NUM_OBS_PER_CHUNCK)):
            cacti.append(Cactus(randint(lim_x1, lim_x2), randint(MIN_OBS_H, MAX_OBS_H)))

class Score:

    def __init__(self):
        self.width, self.height = 150, 50
        self.boarder_x, self.boarder_y = 10, 10
        self.score = 0
        self.pos_x = SCREEN_WIDTH - self.width - self.boarder_x
        self.pos_y = self.boarder_y
    
    def update(self):
        self.score += GAME_SPEED//10
    
    def draw(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 0, 0))  # White color text
        SCREEN.blit(score_text, (self.pos_x, self.pos_y))

class Level:

    def __init__(self, score):
        self.score = score
    
    def update(self):
        if self.score.score < 1000:
            self.level_1()
        elif 1000 <= self.score.score < 3000:
            self.level_2()
        elif 3000 <= self.score.score:
            self.level_3()

    def level_1(self):
        global GAME_SPEED, JX, RX, MAX_NUM_OBS_PER_CHUNCK, MIN_OBS_H, MAX_OBS_H
        GAME_SPEED = 12
        JX = GAME_SPEED
        RX = GAME_SPEED * 60
        MAX_NUM_OBS_PER_CHUNCK = 2
        MIN_OBS_H = 30
        MAX_OBS_H = 60

    def level_2(self):
        global GAME_SPEED, JX, RX, MAX_NUM_OBS_PER_CHUNCK, MIN_OBS_H, MAX_OBS_H
        GAME_SPEED = 16
        JX = GAME_SPEED * 5
        RX = GAME_SPEED * 20
        MAX_NUM_OBS_PER_CHUNCK = 4
        MIN_OBS_H = 50
        MAX_OBS_H = 90

    def level_3(self):
        global GAME_SPEED, JX, RX, MAX_NUM_OBS_PER_CHUNCK, MIN_OBS_H, MAX_OBS_H
        GAME_SPEED = 20
        JX = GAME_SPEED * 5
        RX = GAME_SPEED * 20
        MAX_NUM_OBS_PER_CHUNCK = 8
        MIN_OBS_H = 80
        MAX_OBS_H = 150

class Screen:
    def __init__(self):
        pass

    def update(self,x):
        print(x)

# Check if the masks overlap
def check_collision(dinosaur, cactus):
    frame_rect = dinosaur.cur_frame.get_rect()
    frame_rect.topleft = (dinosaur.pos_x, dinosaur.pos_y)
    cactus_rect = cactus.cur_frame.get_rect()
    cactus_rect.topleft = (cactus.pos_x, cactus.pos_y)
    frame_mask = pygame.mask.from_surface(dinosaur.cur_frame)
    cactus_mask = pygame.mask.from_surface(cactus.cur_frame)
    # Check if the rectangles are colliding first (this is a quick bounding box check)
    if frame_rect.colliderect(cactus_rect):
        # Find the offset (difference in position between the two objects)
        offset = (cactus_rect.x - frame_rect.x, cactus_rect.y - frame_rect.y)
        
        # Check for pixel-level collision using the masks
        if frame_mask.overlap(cactus_mask, offset):
            return True  # There is a collision
    
    return False  # No collision

# Game Initialization
score = Score()
level = Level(score)
dino = Dinosaur(100, 100)
ground = Ground()
obsticals_generator = Obstical()
screen = Screen()
cacti = []

running = True
key_pressed = None
end_game = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            # Check if the window is resized to the full screen size
            if event.w == pygame.display.Info().current_w and event.h == pygame.display.Info().current_h:
                if not fullscreen:
                    # Switch to fullscreen if not already
                    screen = pygame.display.set_mode((event.w, event.h), pygame.FULLSCREEN)
                    fullscreen = True
            else:
                if fullscreen:
                    # Switch back to windowed mode if it's resized and not fullscreen
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    fullscreen = False

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
    obsticals_generator.update()

    to_remove = []
    for cactus in cacti:
        cactus.update()
        if cactus.pos_x < -cactus.width:
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

    for cactus in cacti:
        if check_collision(dino, cactus):
            GAME_SPEED = 0
            end_game = True

    if not end_game:
        score.update()
        level.update()
    score.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()