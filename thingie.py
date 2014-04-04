__author__ = 'Sam'

import pygame
import sys
import pygame.locals
import math

pygame.init()  # initialise pygame

size = width, height = 800, 600  # set size of screen
colour = 100, 20, 30  # colour for background

screen = pygame.display.set_mode(size)  # apply screen size
pygame.display.set_caption('Lord of the Sings')  # set name on screen

clock = pygame.time.Clock()  # sets up a clock to control FPS

myfont = pygame.font.SysFont("monospace", 15)  # set font for later use

walls = []
nodes = []


class Player(pygame.sprite.Sprite):  # create a class named Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialise sprite on self

        self.bitmap = pygame.image.load("OldManSprite.png")  # load image for sprite
        self.player_rect = self.bitmap.get_rect()  # gets rectangular shape of image

        self.hp = 50
        self.strength = 10
        self.dmgmod = 1
        self.speed = 5

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
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.player_rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.player_rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.player_rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.player_rect.top = wall.rect.bottom

    def render(self):  # render function
        screen.blit(self.bitmap, self.shipRect)

    def player_attack(self, target):  # allows player to attack enemy
        player_damage_dealt = self.strength * self.dmgmod
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

    def move_to_player(self, Player):  # makes enemy move towards the player's positio
        dx, dy = player.player_rect.x - self.enemy_rect.x, player.player_rect.y - self.enemy_rect.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        else:
            dx, dy = dx / dist, dy / dist

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
        self.chest_rect.topleft = [100, 200]


class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)


class Node(object):
    def __init__(self, pos):
        nodes.append(self)

level = [  # array to store the level map
"WWWWWWWWWWWWWWWWWWWW",
"WnnnnnnnnnnnnnnnnnnW",
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
"W     W    E   W   W",
"WWWWWWWWWWWWWWWWWWWW",
]

x = y = 0  # sets up map
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "n":
            Node((x, y))
        x += 40
    y += 40
    x = 0

player = Player()  # define player as an instance of class Player
enemy = Enemy()
chest = Chest()

player.player_rect.x = 45  # sets player start position
player.player_rect.y = 450

enemy.enemy_rect.x = 500  # sets enemy start position
enemy.enemy_rect.y = 100

fighting = False

while 1:  # main game loop

    while fighting:  # fighting loop

        if player.speed > enemy.speed:
            player_turn = True
        else:
            player_turn = False

        while player_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # looks for an exit command
                    pygame.quit()  # quits pygame
                    sys.exit()  # closes system

            screen.fill(colour)

            screen.blit(player.bitmap, player.player_rect)
            screen.blit(enemy.bitmap, enemy.enemy_rect)

            player.player_rect.x = 100
            player.player_rect.y = 300

            enemy.enemy_rect.x = 700
            enemy.enemy_rect.y = 300

            player.player_attack(enemy)

            if enemy.hp <= 0:
                fighting = False

            pygame.display.flip()  # updates screen
            clock.tick(30)  # limits fps to 30

            player_turn = False

            break

        while not player_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # looks for an exit command
                    pygame.quit()  # quits pygame
                    sys.exit()  # closes system

            screen.fill(colour)

            screen.blit(player.bitmap, player.player_rect)
            screen.blit(enemy.bitmap, enemy.enemy_rect)

            player.player_rect.x = 100
            player.player_rect.y = 300

            enemy.enemy_rect.x = 700
            enemy.enemy_rect.y = 300

            enemy.enemy_attack(player)

            pygame.display.flip()  # updates screen
            clock.tick(30)  # limits fps to 30

            player_turn = True

            break

    while not fighting:
        label = myfont.render(str(enemy.hp), 1, (255, 255, 0))
        label2 = myfont.render(str(player.hp), 1, (255, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # looks for an exit command
                pygame.quit()  # quits pygame
                sys.exit()  # closes system

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.player_attack(enemy)
                enemy.rebound(200, -300)

        screen.fill(colour)  # fills screen with colour defined above

        screen.blit(player.bitmap, player.player_rect)  # calls blit function on specified classes

        if enemy.dead is False:
            screen.blit(enemy.bitmap, enemy.enemy_rect)

        # screen.blit(chest.bitmap, chest.chest_rect)

        screen.blit(label, (100, 100))
        screen.blit(label2, (100, 50))

        enemy.move_to_player(player)

        for wall in walls:  # draws map to screen
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)

        pygame.display.flip()  # updates screen
        clock.tick(30)  # limits fps to 30