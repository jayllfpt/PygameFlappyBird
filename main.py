import pygame
import sys
import random


def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))

def check_collision(pipes):
    # check pipe is not hit
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    # check floor is not hit
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, 0, 1)
            screen.blit(flip_pipe, pipe)

#   CONSTRAINTS
# WIDTH, HEIGHT = 288, 512
WIDTH, HEIGHT = 576, 1024
BCenterX, BCenterY = 100, 512
MCenterX, MCenterY = 288, 512
PHeight = [400, 600, 800, 700]

pygame.init()
clock = pygame.time.Clock()

gravity = 0.25
bird_movement = 0
# init screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# init background
background = pygame.image.load("flappy-bird-assets/sprites/background-day.png").convert()
background = pygame.transform.scale2x(background)
# init bird
bird = pygame.image.load("flappy-bird-assets/sprites/bluebird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(BCenterX, BCenterY))
# init floor
floor_base = pygame.image.load("flappy-bird-assets/sprites/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0
# init G.O message
message = pygame.image.load("flappy-bird-assets\sprites\message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(MCenterX, MCenterY))
# init pipes
pipe_surface = pygame.image.load("flappy-bird-assets\sprites\pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = PHeight
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# init sounds
flap_sound = pygame.mixer.Sound("flappy-bird-assets/audio/wing.wav")
die_sound = pygame.mixer.Sound("flappy-bird-assets/audio/hit.wav")

game_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (BCenterX, BCenterY)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background, (0, 0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        # draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # check for collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)
    # create floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(90)
