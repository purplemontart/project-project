__author__ = 'Sam'

import pygame
import sys
import pygame.locals
import math
import random
import time

pygame.init()  # initialise pygame
pygame.mixer.init()

music = 'Canon in D 8-bit Chiptune.mp3'

pygame.mixer.music.load(music)
pygame.mixer.music.play(-1, 0.0)

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

size = width, height = 800, 600  # set size of screen
colour = 100, 20, 30  # colour for background

screen = pygame.display.set_mode(size)  # apply screen size
pygame.display.set_caption('Lord of the Sings')  # set title of game window

clock = pygame.time.Clock()  # sets up a clock to control FPS

myfont = pygame.font.SysFont("monospace", 15)  # set font for later use

walls = []  # creates an array called walls


class Player(pygame.sprite.Sprite):  # create a class named Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialise sprite on self

        self.bitmap = pygame.image.load("OldManSprite.png")  # load image for sprite
        self.player_rect = self.bitmap.get_rect()  # gets rectangular shape of image

        self.hp = 50
        self.strength = 10
        self.dmgmod = 1
        self.speed = 5

        self.inventory = []

        self.weaponmod = 0

    def move(self, dx, dy):  # defines player movement
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.player_rect.x += dx
        self.player_rect.y += dy

        for wall in walls:
            if self.player_rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.player_rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.player_rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.player_rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.player_rect.top = wall.rect.bottom

    def render(self):  # render function
        screen.blit(self.bitmap, self.shipRect)

    def player_attack(self, target):  # allows player to attack enemy
        player_damage_dealt = self.strength * self.dmgmod + self.weaponmod
        target.hp -= player_damage_dealt
        return


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bitmap = pygame.image.load("Beetle.png")  # load image for enemy
        self.enemy_rect = self.bitmap.get_rect()
        self.enemy_rect.topleft = [100, 200]
        self.speed = 2

        self.hp = 10
        self.strength = 7
        self.speed = 3
        self.dead = False

    def move_to_player(self, Player):  # makes enemy move towards the player's position
        dx, dy = player.player_rect.x - self.enemy_rect.x, player.player_rect.y - self.enemy_rect.y
        dist = math.hypot(dx, dy)

        if dist == 0:
            dist = 1
        else:
            dx, dy = dx / dist, dy / dist

        if dist < 100:  # means that the enemy will only move towards the player if within the stated distance in pixels
            self.enemy_rect.x += dx * self.speed
            self.enemy_rect.y += dy * self.speed
        return

    def rebound(self, x, y):  # moves enemy away when hit
        self.enemy_rect.centerx += x
        self.enemy_rect.centery += y

    def enemy_attack(self, target):
        enemy_damage_dealt = self.strength
        target.hp -= enemy_damage_dealt
        return


class Chest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bitmap = pygame.image.load("chest.png")
        self.chest_rect = self.bitmap.get_rect()

        self.contents_weapons = ["sword", "bastard sword", "dagger", "stick"]

        self.opened = False

    def open(self):
        if self.opened is False:
            player.inventory.append(random.choice(self.contents_weapons))
            print(player.inventory)

            if "stick" in player.inventory:
                player.weaponmod = 1
            if "dagger" in player.inventory:
                player.weaponmod = 2
            if "sword" in player.inventory:
                player.weaponmod = 3
            if "bastard sword" in player.inventory:
                player.weaponmod = 5

            self.opened = True
        return


class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)


class Node(object):
    def __init__(self, pos):
        nodes.append(self)

level = [  # array to store the level map
"WWWWWWWWWWWWWWWWWWWW",
"W                  W",
"W         WWWWWW   W",
"W   WWWW       W   W",
"W   W        WWWW  W",
"W WWW  WWWW        W",
"W   W     W W      W",
"W   W     W   WWW WW",
"W   WWW WWW   W W  W",
"W     W   W   W W  W",
"WWW   W   WWWWW W  W",
"W W      WW        W",
"W W   WWWW   WWW   W",
"W     W        W   W",
"WWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in level:  # sets up map. for every row in the array...
    for col in row:  # ...and every column in each row...
        if col == "W":  # ...finds every instance of W...
            Wall((x, y))  # ...and creates an instance of the Wall class
        x += 40  # moves along 40 pixels on the x axis
    y += 40  # moves down 40 on the y axis
    x = 0  # resets x to 0

player = Player()  # creates an instance of the Player class called player
enemy = Enemy()
chest = Chest()

player.player_rect.x = 45  # sets player start position
player.player_rect.y = 450

enemy.enemy_rect.x = 500  # sets enemy start position
enemy.enemy_rect.y = 100

chest.chest_rect.x = 42
chest.chest_rect.y = 500

fighting = False

while 1:  # main game loop

    if player.speed > enemy.speed:
        player_turn = True
    else:
        player_turn = False

    while fighting:  # fighting loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # looks for an exit command
                pygame.quit()  # quits pygame
                sys.exit()  # closes system

        screen.fill(colour)

        screen.blit(player.bitmap, player.player_rect)
        screen.blit(enemy.bitmap, enemy.enemy_rect)
        screen.blit(label, (200, 400))

        player.player_rect.x = 100
        player.player_rect.y = 300

        enemy.enemy_rect.x = 700
        enemy.enemy_rect.y = 300

        if enemy.hp <= 0:
            fighting = False
            break
        else:
            key = pygame.key.get_pressed()

            if player_turn:
                label = myfont.render("Press space to attack or enter to wait", 1, (255, 255, 0))

                if key[pygame.K_SPACE]:
                    player.player_attack(enemy)
                    pygame.time.wait(1)
                    player_turn = False
                    if enemy.hp <= 0:
                        break
                elif key[pygame.K_RETURN]:
                    player_turn = False

            if not player_turn:
                label = myfont.render("Press X to continue", 1, (255, 255, 0))
                if key[pygame.K_x]:
                    label = myfont.render("Hit!", 1, (255, 255, 0))
                    enemy.enemy_attack(player)
                    player_turn = True
                elif key[pygame.K_y]:
                    label = myfont.render("Surprise!", 1, (255, 255, 0))
                    player_turn = True

        pygame.display.flip()
        clock.tick(30)

    while not fighting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # looks for an exit command
                pygame.quit()  # quits pygame
                sys.exit()  # closes system

        label = myfont.render(str(enemy.hp), 1, (255, 255, 0))
        label2 = myfont.render(str(player.hp), 1, (255, 255, 0))

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)

        if player.player_rect.colliderect(enemy.enemy_rect):  # sets up player collision with enemy
            fighting = True
            pygame.display.set_caption(str(fighting))

        if player.player_rect.colliderect(chest.chest_rect):
            chest.open()

        screen.fill(colour)  # fills screen with colour defined above

        screen.blit(player.bitmap, player.player_rect)  # calls blit function on specified classes

        if enemy.dead is False:
            screen.blit(enemy.bitmap, enemy.enemy_rect)

        screen.blit(chest.bitmap, chest.chest_rect)

        screen.blit(label, (100, 100))
        screen.blit(label2, (100, 50))

        enemy.move_to_player(player)

        for wall in walls:  # draws map to screen
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)

        pygame.display.flip()  # updates screen
        clock.tick(30)  # limits fps to 30
