import pygame

from Constants import RED, COLOR_RED, GREEN, COLOR_GREEN, YELLOW, COLOR_YELLOW, VERTICAL, HORIZONTAL, NORTH, EAST, \
    LIGHTS_DISTANCE, SOUTH


class TrafficLights:

    def __init__(self, x, y, direction, pos):
        self.x = x
        self.y = y
        self.direction = direction
        self.light = RED
        self.color = COLOR_RED
        self.position = 0
        self.old_light = RED
        #to check if the red light is at the left side or right side
        if pos == NORTH or pos == EAST:
            self.pos_multiplier = -1
        else:
            self.pos_multiplier = 1

        #Hitbox is only useful for sidewalk lights
        if pos == SOUTH or pos == NORTH:
            self.hitbox = pygame.Rect(0, self.y, 1600, 5)
        else:
            self.hitbox = pygame.Rect(self.x + 2 * self.pos_multiplier * LIGHTS_DISTANCE, 0,5,900 )

    def draw(self, win, debug):
        if self.direction == VERTICAL:
            pygame.draw.circle(win, self.color, (self.x, self.y + self.position * LIGHTS_DISTANCE), 5)
        elif self.direction == HORIZONTAL:
            pygame.draw.circle(win, self.color, (self.x + self.position * LIGHTS_DISTANCE, self.y), 5)
        if debug:
            pass #pygame.draw.rect(win, (0,0,0), self.hitbox)

    def setLight(self, light):
        self.old_light = self.light
        self.light = light
        if self.light == RED:
            self.color = COLOR_RED
            self.position = 0 * self.pos_multiplier
        elif self.light == GREEN:
            self.color = COLOR_GREEN
            self.position = 2 * self.pos_multiplier
        elif self.light == YELLOW:
            self.color = COLOR_YELLOW
            self.position = 1 * self.pos_multiplier

    def getLight(self):
        return self.light

    def permute(self):
        if self.getLight() == YELLOW:
            if self.old_light == GREEN:
                self.setLight(RED)
            elif self.old_light == RED:
                self.setLight(GREEN)
        elif self.getLight() == RED or self.getLight() == GREEN:
            self.setLight(YELLOW)
