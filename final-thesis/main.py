# Flappy Bird source code taken from https://github.com/russs123/flappy_bird

import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# LOADING ALL IMAGES
background_img = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    return score



# GAME VARIABLES
font = pygame.font.SysFont('Bauhaus 93', 60)
# define color
white = (255, 255, 255)
scroll_ground = 0
# every itteration ground moves by 4 pixels
scroll_speed = 4  
# not start the game imediately 
flying = False
# check for game over
dead = False
# gap in between the pipes
pipe_gap = 170
# how often new pipes spawn 1500 milliseconds
pipe_frequency = 1500
# whenever the game is first initialized
last_pipe = pygame.time.get_ticks() - pipe_frequency
# keep track of core
score = 0
# check if a pipe has been surpased
pass_pipe = False


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # inheriting update and draw functins from pygame.Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            bird_img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(bird_img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # add gravity
        self.velocity = 0
        self.clicked = False


    # update function handles the bird animation
    def update(self):

        if flying == True:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)

        if dead == False:
            # handle flapping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10

            # only being able to flap once mouse has been released 
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cool_down = 5

            if self.counter > flap_cool_down:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], -2 * self.velocity)
        else:
            # the bird faces the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    
    def draw(self):
        action = False
        # get mouse position
        position = pygame.mouse.get_pos()

        # check if mouse is over the button
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw restart button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# bird group keeps track of all the sprites added to it
bird_group = pygame.sprite.Group()

# pipe group keeps track of all the pipes added 
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))

bird_group.add(flappy)

# create restart button instance
button = Button(screen_width // 2 - 60, screen_height // 2 + 350, button_img)

run = True
# game starts running, while not interrupted
while run:   

    clock.tick(fps)

    # in pygame we use blit to display images
    screen.blit(background_img, (0, 0))    

    # draw bird
    bird_group.draw(screen)
    bird_group.update()

    # draw pipes
    pipe_group.draw(screen)

    # create the ground to be scrolable
    screen.blit(ground_img, (scroll_ground, 768))
    if len(pipe_group) == 0:
        pipe_height = random.randint(-100, 100)
        initial_bottom_pipe = Pipe(screen_width - 400, int(screen_height / 2) + pipe_height, -1)
        initial_top_pipe = Pipe(screen_width - 400, int(screen_height/2) + pipe_height, 1)
        pipe_group.add(initial_bottom_pipe)
        pipe_group.add(initial_top_pipe)

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and  bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 25)

    # check if the bird has hit a pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        dead = True


    # check if the bird has hit the gtound
    if flappy.rect.bottom >= 768:
        dead = True
        flying = False  
    
    # game is running
    if dead == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        scroll_ground -= scroll_speed
        # once it exceeds the screen width, restart image position
        if abs(scroll_ground) > 35:
            scroll_ground = 0 

        pipe_group.update()
    

    # check if game over and reset
    if dead == True:
        if button.draw() == True:
            dead = False
            score = reset_game()


    # key event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and dead == False:
            flying = True

    # nothing gets displayed unless we update the screen
    pygame.display.update()    


pygame.quit()

