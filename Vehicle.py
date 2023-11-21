from math import sin, radians, degrees

import pygame
from pygame.math import Vector2

from Constants import NORTH, SOUTH, EAST, WEST, NO_STEERING, STEERING_LEFT, STEERING_RIGHT, WIDTH, HEIGHT, PPU
from Physics import Physics


class Vehicle:
    number = 0
    def __init__(self, ini_pos, final_pos):
        self.ini_pos = ini_pos
        self.final_pos = final_pos
        self.position = Vector2(0, 0)
        self.back_position = Vector2(0, 0)
        self.image = None
        self.rotated = None
        self.velocity = Vector2(0, 0)
        self.default_velocity = self.velocity
        self.stop_velocity = Vector2(0, 0)
        self.angle = 0
        self.turn_position = Vector2(0, 0)
        self.steering = 0
        self.turning = 0
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.mask = None
        self.deciding_light = 0
        self.hitbox_preview = pygame.Rect(0, 0, 0, 0)
        self.start_time = pygame.time.get_ticks()
        # depending on the initial position, car must be rotated
        # checking what to do to get to the final position (continue straight, turn left or turn right)
        if ini_pos == NORTH:
            self.angle = 270
            if final_pos == SOUTH:
                self.steering_at_O_position = NO_STEERING
            elif final_pos == WEST:
                self.steering_at_O_position = STEERING_RIGHT
            elif final_pos == EAST:
                self.steering_at_O_position = STEERING_LEFT
        if ini_pos == WEST:
            self.angle = 0
            if final_pos == SOUTH:
                self.steering_at_O_position = STEERING_RIGHT
            elif final_pos == EAST:
                self.steering_at_O_position = NO_STEERING
            elif final_pos == NORTH:
                self.steering_at_O_position = STEERING_LEFT
        if ini_pos == EAST:
            self.angle = 180
            if final_pos == SOUTH:
                self.steering_at_O_position = STEERING_LEFT
            elif final_pos == WEST:
                self.steering_at_O_position = NO_STEERING
            elif final_pos == NORTH:
                self.steering_at_O_position = STEERING_RIGHT
        if ini_pos == SOUTH:
            self.angle = 90
            if final_pos == NORTH:
                self.steering_at_O_position = NO_STEERING
            elif final_pos == WEST:
                self.steering_at_O_position = STEERING_LEFT
            elif final_pos == EAST:
                self.steering_at_O_position = STEERING_RIGHT
        self.old_angle = self.angle
        # if the final position is the same as the initial, we'll just delete the car
        if ini_pos == final_pos:
            del self
        Vehicle.number += 1

    def draw(self, win, debug):
        rotated = pygame.transform.rotate(self.image, self.angle)
        if debug:
            pygame.draw.rect(win, (115,115,115), self.hitbox)

        win.blit(rotated, self.position * PPU)

    def isOutOfScreen(self):
        return Physics.outOfScreen(self.hitbox, WIDTH, HEIGHT)

    def move(self, dt):
        if self.isAtTurningPosition() and self.turning == 0:
            self.ChangeDirection()

        if self.steering != 0:
            turning_radius = self.image.get_width() / 40 / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += round(degrees(angular_velocity) * dt)
        self.BackPosition()

        #angle range
        if self.turning == 1 and (abs(abs(self.angle) - abs(self.old_angle)) > 90):
            if self.angle < -180:
                self.angle = -180
            elif 170 < self.angle < 190:
                self.angle = 180
            elif 80 < self.angle < 100:
                self.angle = 90
            elif -15 < self.angle < 15:
                self.angle = 0
            elif 260 < self.angle < 280:
                self.angle = 270
            elif 350 < self.angle < 370:
                self.angle = 360
        #finished turning
        if self.angle % 90 == 0 and int(self.old_angle) != int(self.angle):
            self.old_angle = 0
            self.steering = 0
            self.angle = int(self.angle)
            if abs(self.angle) == 360:
                self.angle = 0
            self.turning = -1
        self.setHitbox()
        self.getHitboxPreview(dt)

    def setHitbox(self):
        if 45 < self.angle < 135:
            self.hitbox.x = self.position.x * PPU
            self.hitbox.y = self.position.y * PPU - 20
            self.hitbox.h = self.image.get_width() + 20
            self.hitbox.w = self.image.get_height()
        elif 134 < self.angle < 225:
            self.hitbox.x = self.position.x * PPU - 20
            self.hitbox.y = self.position.y * PPU
            self.hitbox.w = self.image.get_width() + 20
            self.hitbox.h = self.image.get_height()
        else:
            self.hitbox.x = self.position.x * PPU
            self.hitbox.y = self.position.y * PPU
            if 45 > self.angle > -45 or 405 > self.angle > 315:
                self.hitbox.w = self.image.get_width() + 20
                self.hitbox.h = self.image.get_height()
            else:
                self.hitbox.h = self.image.get_width() + 20
                self.hitbox.w = self.image.get_height()

    def getHitboxPreview(self, dt):
        pos = (self.position + self.velocity.rotate(-self.angle) * dt) * PPU
        self.hitbox_preview = pygame.Rect(0, 0, 0, 0)
        if 45 < self.angle < 135:
            self.hitbox_preview.x = pos.x
            self.hitbox_preview.y = pos.y - 20
            self.hitbox_preview.h = self.image.get_width() + 20
            self.hitbox_preview.w = self.image.get_height()
        elif 134 < self.angle < 225:
            self.hitbox_preview.x = pos.x - 20
            self.hitbox_preview.y = pos.y
            self.hitbox_preview.w = self.image.get_width() + 20
            self.hitbox_preview.h = self.image.get_height()
        else:
            self.hitbox_preview.x = pos.x
            self.hitbox_preview.y = pos.y
            if 45 > self.angle > -45:
                self.hitbox_preview.w = self.image.get_width() + 20
                self.hitbox_preview.h = self.image.get_height()
            else:
                self.hitbox_preview.h = self.image.get_width() + 20
                self.hitbox_preview.w = self.image.get_height()

        '''if self.angle == 0 or abs(self.angle) == 180:
            self.hitbox_preview.w = self.image.get_width() + 30
            self.hitbox_preview.h = self.image.get_height()
        else:
            self.hitbox_preview.h = self.image.get_width() + 30
            self.hitbox_preview.w = self.image.get_height()'''
        return self.hitbox_preview

    def BackPosition(self):
        if self.angle == 0 or self.angle == -90 or self.angle == 270:
            self.back_position = Vector2(self.position.x * 32, self.position.y * 32)
        elif sin(self.angle) == 1 or self.angle == 90 or self.angle == -270:
            self.back_position = Vector2(self.position.x * 32, self.position.y * 32 + self.image.get_width())
        elif abs(self.angle) == 180:
            self.back_position = Vector2(self.position.x * 32 + self.image.get_width(), self.position.y * 32)

    def ChangeDirection(self):
        self.steering = self.steering_at_O_position
        self.turning = 1
        self.old_angle = self.angle

    def isAtTurningPosition(self):
        return self.hitbox.collidepoint((self.turn_position.x, self.turn_position.y))

    def stop(self):
        if not self.deciding_light:
            self.deciding_light = False
            self.velocity = self.stop_velocity

    def go(self):
        self.velocity = self.default_velocity
        self.deciding_light = True

    def yellow_light(self):
        self.stop()

    def setStartTime(self, time):
        self.start_time = time

    def getStartTime(self):
        return self.start_time
