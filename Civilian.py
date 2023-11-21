import pygame
import copy
from pygame import Vector2
from Constants import HORIZONTAL, VERTICAL, WIDTH, HEIGHT, UP, DOWN, LEFT, RIGHT
from Media import PERSON_1_STANDING, PERSON_1
from Physics import Physics


class Civilian:
    number = 0
    def __init__(self, position, direction, vel):
        self.position = position
        self.image = PERSON_1_STANDING
        self.index = 0
        self.crossing = False
        self.direction = direction
        self.speed = vel
        self.mask = pygame.mask.from_surface(self.image)
        self.start_time = 0
        if self.direction == HORIZONTAL:
            if self.speed > 0:
                self.animation = RIGHT
                self.angle = 0
            else:
                self.animation = LEFT
                self.angle = 180
        if self.direction == VERTICAL:
            if self.speed > 1:
                self.animation = DOWN
                self.angle = -90
            else:
                self.animation = UP
                self.angle = 90

        self.default_speed = 4
        self.hitbox = pygame.Rect((self.position.x, self.position.y, self.image.get_width(), self.image.get_height()))
        self.changed_direction = False
        Civilian.number += 1

    def draw(self, win, debug):
        if debug:
            pygame.draw.rect(win, (115,115,115), self.hitbox)
        win.blit(self.image, self.position)

    def move(self):
        self.index += 1
        if self.index == 12:
            self.index = 0
        if self.speed != 0:
            self.image = PERSON_1[self.index]
            if self.direction == HORIZONTAL:
                self.position.x += self.speed
            elif self.direction == VERTICAL:
                self.position.y += self.speed
            self.rotateImage()
        self.hitbox = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())

    def getHitboxPreview(self):
        pos_before_preview = copy.copy(self.position)
        if self.direction == HORIZONTAL:
            self.position.x += self.speed
        elif self.direction == VERTICAL:
            self.position.y += self.speed
        hitbox_preview = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
        self.position = pos_before_preview
        return hitbox_preview

    def rotateImage(self):
        if self.animation == LEFT:
            self.angle = 180
        elif self.animation == UP:
            self.angle = 90
        elif self.animation == DOWN:
            self.angle = -90
        elif self.animation == RIGHT:
            self.angle = 0

        self.image = pygame.transform.rotate(self.image, self.angle)

    def stop(self):
        self.speed = 0
        self.setStanding()

    def yellow_light(self, zone):
        if zone == 1:
            self.speed = self.default_speed * -2
        if zone == 0:
            self.speed = self.default_speed * 2

    def go(self, zone):
        if zone == 1:
            self.speed = self.default_speed * -1
        if zone == 0:
            self.speed = self.default_speed

    def changeDirection(self, zone):
        if self.direction == HORIZONTAL:
            self.direction = VERTICAL
            if zone == 0:
                self.animation = DOWN
            else:
                self.animation = UP
        else:
            self.direction = HORIZONTAL
            if zone == 0:
                self.animation = RIGHT
            else:
                self.animation = LEFT

        self.changed_direction = True

    def setDirection(self, direction):
        self.direction = direction

    def isOutOfScreen(self):
        return Physics.outOfScreen(self.hitbox, WIDTH, HEIGHT)

    def setStartTime(self, time):
        self.start_time = time

    def getStartTime(self):
        return self.start_time

    def setStanding(self):
        self.image = PERSON_1_STANDING
        self.rotateImage()
