__author__ = 'Sam'

import pygame
import sys
import pygame.locals

pygame.init()  # initialise pygame

size = width, height = 800, 500  # set size of screen
colour = 100, 20, 30  # colour for background

screen = pygame.display.set_mode(size)  # apply screen size
pygame.display.set_caption('Lord of the Sings')  # set name on screen

class Player(pygame.sprite.Sprite): # create a class named Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialise sprite on self

        self.bitmap = pygame.image.load("ball.bmp")  # load image for sprite
        self.shipRect = self.bitmap.get_rect()  # gets rectangular shape of image
        self.shipRect.topleft = [100, 200]

    def move(self, x, y):  # defines movement function
        self.shipRect.centerx += x
        self.shipRect.centery += y

    def render(self):  # render function
        screen.blit(self.bitmap, (self.shipRect))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bitmap = pygame.image.load("ball.bmp")
        self.enemy_rect = self.bitmap.get_rect()
        self.enemy_rect.topleft = [100, 200]

player = Player()  # define player as an instance of class Player
enemy = Enemy()

while 1:  # main game loop

    count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # looks for an exit command
            sys.exit()  # if found, exits the program

        if event.type == pygame.KEYDOWN:  # allows for movement control via keyboard
            if event.key == pygame.K_DOWN:
                player.move(0, 5)
            if event.key == pygame.K_UP:
                player.move(0, -5)
            if event.key == pygame.K_LEFT:
                player.move(-5, 0)
            if event.key == pygame.K_RIGHT:
                player.move(5, 0)

        if player.shipRect.colliderect(enemy.enemy_rect):
            pygame.display.set_caption('Hit!')

    screen.fill(colour)  # fills screen with colour defined above
    screen.blit(player.bitmap, player.shipRect)  # calls blit function on specified items
    screen.blit(enemy.bitmap, enemy.enemy_rect)
    pygame.display.flip()  # updates screen