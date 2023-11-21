import random

import pygame
from pygame import Vector2

from Constants import INITIAL_POSITION, TURN_POSITION, PPU, UNDEF_POSITION
from Media import SPORTS_CAR_ICONS
from Vehicle import Vehicle


class SportsCar(Vehicle):

    def __init__(self, ini_pos, final_pos, terrain):
        super().__init__(ini_pos, final_pos)

        coordinates = terrain.getCoordinates(ini_pos, final_pos)
        if coordinates == UNDEF_POSITION:
            del self
            return

        self.ini_pos = coordinates[INITIAL_POSITION]
        self.position = self.ini_pos / PPU
        self.image = SPORTS_CAR_ICONS[random.randint(0,3)]
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = Vector2(5.0, 0.0)
        self.default_velocity = self.velocity
        self.old_angle = self.angle
        self.back_position = Vector2(0.0, 0.0)
        self.turning = 0
        self.crossed_yellow_light = 0
        self.setHitbox()
        self.turn_position = coordinates[TURN_POSITION]

    def yellow_light(self):
        if self.crossed_yellow_light == 0:
            if random.randint(1, 2) == 1:
                self.go()
                self.crossed_yellow_light = 1
            else:
                self.stop()
                self.crossed_yellow_light = -1
