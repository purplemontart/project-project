__author__ = 'Sam'

import pygame
import sys
import pygame.locals

pygame.init()

size = width, height = 800, 500
colour = 100, 20, 30

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Lord of the Sings')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [2, 2]

        self.bitmap = pygame.image.load("ball.bmp")
        self.bitmap.set_colorkey((0, 0, 0))
        self.shipRect = self.bitmap.get_rect()
        self.shipRect.topleft = [100, 200]

    def move(self, x, y):
        self.shipRect.centerx += x
        self.shipRect.centery += y

    def render(self):
        screen.blit(self.bitmap, (self.shipRect))

player = Player()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.move(0, 5)
            if event.key == pygame.K_UP:
                player.move(0, -5)
            if event.key == pygame.K_LEFT:
                player.move(-5, 0)
            if event.key == pygame.K_RIGHT:
                player.move(5, 0)

    screen.fill(colour)
    screen.blit(player.bitmap, player.shipRect)
    pygame.display.flip()