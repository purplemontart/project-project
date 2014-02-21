__author__ = 'Sam'

import pygame
import sys
import pygame.locals
import math

pygame.init()  # initialise pygame

size = width, height = 800, 500  # set size of screen
colour = 100, 20, 30  # colour for background

screen = pygame.display.set_mode(size)  # apply screen size
pygame.display.set_caption('Lord of the Sings')  # set name on screen

class Player(pygame.sprite.Sprite): # create a class named Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialise sprite on self

        self.bitmap = pygame.image.load("ball.bmp")  # load image for sprite
        self.player_rect = self.bitmap.get_rect()  # gets rectangular shape of image
        self.player_rect.topleft = [100, 200]

        self.hp = 50
        self.strength = 10
        self.dmgmod = 0

    def move(self, x, y):  # defines movement function
        self.player_rect.centerx += x
        self.player_rect.centery += y

    def render(self):  # render function
        screen.blit(self.bitmap, (self.shipRect))

    def player_attack(self, target):
        player_damage_dealt = self.strength * self.dmgmod
        target.hp -= player_damage_dealt
        return

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bitmap = pygame.image.load("ball.bmp")
        self.enemy_rect = self.bitmap.get_rect()
        self.enemy_rect.topleft = [100, 200]
        self.speed = 1

        self.hp = 10
        self.strength = 7

    def move_to_player(self, Player):
        dx, dy = player.player_rect.x - self.enemy_rect.x, player.player_rect.y - self.enemy_rect.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist == 1
        else:
            dx, dy = dx / dist, dy / dist

        self.enemy_rect.x += dx * self.speed
        self.enemy_rect.y += dy * self.speed
        return

player = Player()  # define player as an instance of class Player
enemy = Enemy()

player.player_rect.x = 50
player.player_rect.y = 300

enemy.enemy_rect.x = 500
enemy.enemy_rect.y = 100

while 1:  # main game loop
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

        if player.player_rect.colliderect(enemy.enemy_rect):
            pygame.display.set_caption('Hit!')
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.player_attack(enemy)
            

    screen.fill(colour)  # fills screen with colour defined above
    screen.blit(player.bitmap, player.player_rect)  # calls blit function on specified classes
    screen.blit(enemy.bitmap, enemy.enemy_rect)
    enemy.move_to_player(player)
    pygame.display.flip()  # updates screen
