import json
import os
import sys
import pygame
from pygame.math import Vector2

from Constants import NORTH, SOUTH, EAST, WEST, HORIZONTAL, VERTICAL, ENTRANCE, EXIT, FREE_ZONE, RED, GREEN, WIDTH, \
    HEIGHT, UNDEF_POSITION, CIVILIAN_WIDTH, CIVILIAN_HEIGHT, YELLOW
from TrafficLights import TrafficLights


class Map:
    UNDEFINED_HITBOX = pygame.Rect(WIDTH * -1, HEIGHT * -1, 0, 0)

    def __init__(self, file_name):
        self.file_path = os.path.join('assets\map', file_name + '.json')
        self.image_path = os.path.join('assets\map', file_name + '.png')
        self.traffic_lights = [None,None,None,None]
        self.sidewalk_lights = [None,None,None,None]
        self.coordinates_lst = [[], [], [], []]
        self.lane_exists = [False, False, False, False]

        # map hitboxes
        self.general_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX,
                               self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.north_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.south_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.west_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.east_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.entrance_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX,
                                self.UNDEFINED_HITBOX]
        self.exit_hitbox = [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]
        self.free_zone_hitbox = self.UNDEFINED_HITBOX

        self.sidewalk_hitbox = [[self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX],
                                [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX],
                                [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX],
                                [self.UNDEFINED_HITBOX, self.UNDEFINED_HITBOX]]

        # Getting data from json file
        try:
            with open(self.file_path) as r:
                map_data = json.load(r)
        except:
            print()
            print("-------------------------------------------------")
            print("ERROR 101: " + self.file_path + " not found")
            print("-------------------------------------------------")
            sys.exit()
        try:
            self.image = pygame.transform.scale(pygame.image.load(self.image_path), (WIDTH, HEIGHT))
        except:
            print()
            print("-------------------------------------------------")
            print("ERROR 102: " + self.image_path + " not found")
            print("-------------------------------------------------")
            sys.exit()

        self.generate_traffic_lights(map_data)
        self.generate_hitboxes(map_data)
        self.generate_coordinates()
        print('........................')
        print("Successful Map Loading !")
        print('........................')

    def generate_traffic_lights(self, map_data):
        # iterating through every traffic light
        for i in range(len(map_data['traffic_lights'])):
            aux = map_data['traffic_lights'][i]

            if type(aux['direction']) == str:
                if "h" in aux['direction']:
                    aux['direction'] = HORIZONTAL
                elif "v" in aux['direction']:
                    aux['direction'] = VERTICAL

            if type(aux['position']) == str:
                if "n" in aux['position']:
                    aux['position'] = NORTH
                elif "w" in aux['position']:
                    aux['position'] = WEST
                elif "e" in aux['position']:
                    aux['position'] = EAST
                elif "s" in aux['position']:
                    aux['position'] = SOUTH
            self.traffic_lights[aux['position']] = TrafficLights(aux['x'], aux['y'], aux['direction'], aux['position'])

        # iterating through every side walk light
        for i in range(len(map_data['side_walk_lights'])):
            aux = map_data['side_walk_lights'][i]

            if type(aux['direction']) == str:
                if "h" in aux['direction']:
                    aux['direction'] = HORIZONTAL
                elif "v" in aux['direction']:
                    aux['direction'] = VERTICAL

            if type(aux['position']) == str:
                if "n" in aux['position']:
                    aux['position'] = NORTH
                elif "w" in aux['position']:
                    aux['position'] = WEST
                elif "e" in aux['position']:
                    aux['position'] = EAST
                elif "s" in aux['position']:
                    aux['position'] = SOUTH
            self.sidewalk_lights[aux['position']] = [TrafficLights(aux['x1'], aux['y1'], aux['direction'], aux['position']),
                                                     TrafficLights(aux['x2'], aux['y2'], aux['direction'], aux['position'])]

    def generate_hitboxes(self, map_data):
        # north
        if map_data['north']['exists']:
            self.lane_exists[NORTH] = True
            self.north_hitbox = [pygame.Rect(map_data['north']['hitbox_entrance']),
                                 pygame.Rect(map_data['north']['hitbox_exit'])]
            self.general_hitbox[NORTH] = pygame.Rect(map_data['north']['hitbox'])
            self.sidewalk_hitbox[NORTH] = [pygame.Rect(map_data['north']["hitbox_walk_west"]),
                                           pygame.Rect(map_data['north']["hitbox_walk_east"])]
        # west
        if map_data['west']['exists']:
            self.lane_exists[WEST] = True
            self.west_hitbox = [pygame.Rect(map_data['west']['hitbox_entrance']),
                                pygame.Rect(map_data['west']['hitbox_exit'])]
            self.general_hitbox[WEST] = pygame.Rect(map_data['west']['hitbox'])
            self.sidewalk_hitbox[WEST] = [pygame.Rect(map_data['west']["hitbox_walk_north"]),
                                          pygame.Rect(map_data['west']["hitbox_walk_south"])]
        # east
        if map_data['east']['exists']:
            self.lane_exists[EAST] = True
            self.east_hitbox = [pygame.Rect(map_data['east']['hitbox_entrance']),
                                pygame.Rect(map_data['east']['hitbox_exit'])]
            self.general_hitbox[EAST] = pygame.Rect(map_data['east']['hitbox'])
            self.sidewalk_hitbox[EAST] = [pygame.Rect(map_data['east']["hitbox_walk_north"]),
                                          pygame.Rect(map_data['east']["hitbox_walk_south"])]
        # south
        if map_data['south']['exists']:
            self.lane_exists[SOUTH] = True
            self.south_hitbox = [pygame.Rect(map_data['south']['hitbox_entrance']),
                                 pygame.Rect(map_data['south']['hitbox_exit'])]
            self.general_hitbox[SOUTH] = pygame.Rect(map_data['south']['hitbox'])
            self.sidewalk_hitbox[SOUTH] = [pygame.Rect(map_data['south']["hitbox_walk_north"]),
                                           pygame.Rect(map_data['sout']["hitbox_walk_south"])]

        self.free_zone_hitbox = pygame.Rect(map_data['free_region']['hitbox'])
        self.general_hitbox[FREE_ZONE] = self.free_zone_hitbox

        self.entrance_hitbox = [self.north_hitbox[ENTRANCE],
                                self.west_hitbox[ENTRANCE],
                                self.east_hitbox[ENTRANCE],
                                self.south_hitbox[ENTRANCE]]

        self.exit_hitbox = [self.north_hitbox[EXIT],
                            self.west_hitbox[EXIT],
                            self.east_hitbox[EXIT],
                            self.south_hitbox[EXIT]]

    def generate_coordinates(self):
        if not self.general_hitbox[NORTH] == self.UNDEFINED_HITBOX:
            north_west_coordinates = [Vector2(self.entrance_hitbox[NORTH].x + 10, self.entrance_hitbox[NORTH].y),
                                      Vector2(self.entrance_hitbox[NORTH].x + 10, self.exit_hitbox[WEST].y + 64)]

            north_east_coordinates = [Vector2(self.exit_hitbox[NORTH].x - 70, self.entrance_hitbox[NORTH].y),
                                      Vector2(self.exit_hitbox[NORTH].x - 70, self.exit_hitbox[EAST].y + 54)]

            north_south_coordinates = [Vector2((self.entrance_hitbox[NORTH].x + self.exit_hitbox[NORTH].x) // 2,
                                               self.entrance_hitbox[NORTH].y),
                                       Vector2(WIDTH * -1, HEIGHT * -1)]

            north_coordinates = [[], north_west_coordinates, north_east_coordinates, north_south_coordinates]
            self.coordinates_lst[NORTH] = north_coordinates

        if not self.general_hitbox[WEST] == self.UNDEFINED_HITBOX:
            west_north_coordinates = [Vector2(self.entrance_hitbox[WEST].x, self.entrance_hitbox[WEST].y + 10),
                                      Vector2(self.exit_hitbox[NORTH].x + 64, self.entrance_hitbox[WEST].y + 10)]

            west_east_coordinates = [Vector2(self.entrance_hitbox[WEST].x,
                                             self.entrance_hitbox[WEST].y + self.entrance_hitbox[WEST].h - 69),
                                     Vector2(WIDTH * -1, HEIGHT * -1)]

            west_south_coordinates = [Vector2(self.entrance_hitbox[WEST].x, self.entrance_hitbox[WEST].y + self.entrance_hitbox[WEST].h - 74),
                                      Vector2(self.exit_hitbox[SOUTH].x + 64, self.entrance_hitbox[WEST].y + self.entrance_hitbox[WEST].h - 74)]

            west_coordinates = [west_north_coordinates, [], west_east_coordinates, west_south_coordinates]
            self.coordinates_lst[WEST] = west_coordinates

        if not self.general_hitbox[EAST] == self.UNDEFINED_HITBOX:
            east_north_coordinates = [Vector2(self.entrance_hitbox[EAST].x + self.entrance_hitbox[EAST].w - 200,
                                              self.entrance_hitbox[EAST].y + 10),
                                      Vector2(self.exit_hitbox[NORTH].x + 150,
                                              self.entrance_hitbox[EAST].y + 10)]

            east_west_coordinates = [Vector2(self.entrance_hitbox[EAST].x + self.entrance_hitbox[EAST].w - 200,
                                             self.exit_hitbox[EAST].y - 74),
                                     Vector2(WIDTH * -1, HEIGHT * -1)]

            east_south_coordinates = [Vector2(self.entrance_hitbox[EAST].x + self.entrance_hitbox[EAST].w - 200,
                                              self.exit_hitbox[EAST].y - 64),
                                      Vector2(self.exit_hitbox[SOUTH].x + 35, self.exit_hitbox[EAST].y - 64)]

            east_coordinates = [east_north_coordinates, east_west_coordinates, [], east_south_coordinates]
            self.coordinates_lst[EAST] = east_coordinates

        if not self.general_hitbox[SOUTH] == self.UNDEFINED_HITBOX:
            south_north_coordinates = [Vector2((self.entrance_hitbox[SOUTH].x + self.entrance_hitbox[SOUTH].w) - 64,
                                               self.entrance_hitbox[SOUTH].y + self.entrance_hitbox[SOUTH].h - 200),
                                       Vector2(WIDTH * -1, HEIGHT * -1)]

            south_west_coordinates = [Vector2(self.entrance_hitbox[SOUTH].x,
                                              self.entrance_hitbox[SOUTH].y + self.entrance_hitbox[SOUTH].h - 200),
                                      Vector2(self.entrance_hitbox[SOUTH].x, self.exit_hitbox[WEST].y + 54)]

            south_east_coordinates = [Vector2(self.entrance_hitbox[SOUTH].x + self.entrance_hitbox[SOUTH].w - 64,
                                              self.entrance_hitbox[SOUTH].y + self.entrance_hitbox[SOUTH].h - 200),
                                      Vector2(self.entrance_hitbox[SOUTH].x + self.entrance_hitbox[SOUTH].w - 64,
                                              self.exit_hitbox[EAST].y + 180)]

            south_coordinates = [south_north_coordinates, south_west_coordinates, south_east_coordinates]
            self.coordinates_lst[SOUTH] = south_coordinates

    def getCoordinates(self, ini_pos, final_pos):
        if self.lane_exists[ini_pos] and self.lane_exists[final_pos]:
            return self.coordinates_lst[ini_pos][final_pos]
        return UNDEF_POSITION

    def getSideWalkSpawnCoordinates(self, position):
        if self.lane_exists[position[0]]:
            pos = [position[0], position[1]]
            if pos[0] == pos[1]:
                return UNDEF_POSITION
            if pos[0] == NORTH and pos[1] == SOUTH:
                return UNDEF_POSITION
            if pos[0] == WEST and pos[1] == EAST:
                return UNDEF_POSITION
            if pos[0] == SOUTH and pos[1] == NORTH:
                return UNDEF_POSITION
            if pos[0] == EAST and pos[1] == WEST:
                return UNDEF_POSITION
            if pos[0] == NORTH:
                pos[1] -=1
                return Vector2(self.sidewalk_hitbox[NORTH][pos[1]][0], self.sidewalk_hitbox[NORTH][pos[1]][1])
            elif pos[0] == WEST:
                if pos[1] == SOUTH:
                    pos[1] = 1
                return Vector2(self.sidewalk_hitbox[WEST][pos[1]][0], self.sidewalk_hitbox[WEST][pos[1]][1])
            elif pos[0] == EAST:
                if pos[1] == SOUTH:
                    pos[1] = 1
                return Vector2(self.sidewalk_hitbox[EAST][pos[1]][0] + self.sidewalk_hitbox[EAST][pos[1]][2] - CIVILIAN_WIDTH,
                               self.sidewalk_hitbox[EAST][pos[1]][1])
            elif pos[0] == SOUTH:
                pos[1] -= 1
                return Vector2(self.sidewalk_hitbox[EAST][pos[1]][0],
                               self.sidewalk_hitbox[EAST][pos[1]][1] +self.sidewalk_hitbox[EAST][pos[1]][3] - CIVILIAN_HEIGHT)
        return UNDEF_POSITION

    # Draw
    def draw(self, win, debug):
        win.blit(self.image, (0, 0))
        for lights in self.traffic_lights:
            if lights is not None:
                lights.draw(win, debug)
        for pos in self.sidewalk_lights:
            if pos is not None:
                for light in pos:
                    light.draw(win, debug)

        if debug:
            for rect in self.north_hitbox:
                pygame.draw.rect(win, (0, 0, 255), rect, 1)
            for rect in self.west_hitbox:
                pygame.draw.rect(win, (255, 0, 0), rect, 1)
            for rect in self.east_hitbox:
                pygame.draw.rect(win, (0, 255, 0), rect, 1)
            for rect in self.south_hitbox:
                pygame.draw.rect(win, (150, 150, 150), rect, 1)
            pygame.draw.rect(win, (0, 0, 0), self.free_zone_hitbox, 1)
            for pos in self.sidewalk_hitbox:
                for s in pos:
                    pygame.draw.rect(win, (0,150,0),s, 1)

    # Cars and Traffic
    def getNumberOfCarsInLane(self, lane, cars, direction=-1):
        if lane == FREE_ZONE or self.lane_exists[lane]:
            car_hitboxes = []
            for car in cars:
                car_hitboxes.append(car.hitbox)
            if direction == -1:
                if lane == FREE_ZONE:
                    return len(self.free_zone_hitbox.collidelistall(car_hitboxes))
                else:
                    return len(self.general_hitbox[lane].collidelistall(car_hitboxes))
            elif lane == NORTH:
                return len(self.north_hitbox[direction].collidelistall(car_hitboxes))
            elif lane == WEST:
                return len(self.west_hitbox[direction].collidelistall(car_hitboxes))
            elif lane == EAST:
                return len(self.east_hitbox[direction].collidelistall(car_hitboxes))
            elif lane == SOUTH:
                return len(self.south_hitbox[direction].collidelistall(car_hitboxes))
            elif lane == FREE_ZONE:
                return len(self.free_zone_hitbox.collidelistall(car_hitboxes))
        return 0

    def getInTrafficLight(self, car):
        index = car.hitbox.collidelist(self.entrance_hitbox)
        if index != -1 and car.hitbox.colliderect(self.free_zone_hitbox):
            return True
        return False

    def getLane(self, car):
        index = car.hitbox.collidelist(self.general_hitbox)
        if index == NORTH:
            if car.hitbox.colliderect(self.north_hitbox[EXIT]):
                direction = EXIT
            else:
                direction = ENTRANCE
        elif index == WEST:
            if car.hitbox.colliderect(self.west_hitbox[EXIT]):
                direction = EXIT
            else:
                direction = ENTRANCE
        elif index == EAST:
            if car.hitbox.colliderect(self.east_hitbox[EXIT]):
                direction = EXIT
            else:
                direction = ENTRANCE
        elif index == SOUTH:
            if car.hitbox.colliderect(self.south_hitbox[EXIT]):
                direction = EXIT
            else:
                direction = ENTRANCE
        elif index == FREE_ZONE:
            direction = FREE_ZONE
        else:
            direction = -1  # should never happen
        return [index, direction]

    # Traffic Lights
    def setTrafficLight(self, position, light):
        if self.lane_exists[position]:
            self.traffic_lights[position].setLight(light)


    def getTrafficLight(self, position):
        if self.lane_exists[position]:
            return self.traffic_lights[position].getLight()
        return None

    def toggleTrafficLight(self, position):
        if self.lane_exists[position]:
            if self.getTrafficLight(position) == RED:
                self.setTrafficLight(position, GREEN)
            else:
                self.setTrafficLight(position, RED)

    def permuteTrafficLight(self, position):
        if self.lane_exists[position]:
            self.traffic_lights[position].permute()

    #Side Walk
    #Get person's position
    def getSideWalk(self, person):
        for i in range(4):
            aux = person.hitbox.collidelist(self.sidewalk_hitbox[i])
            if aux != -1:
                return i, aux
        return -1, -1

    def getInSideWalkLight(self, person, lane):
        if self.lane_exists[lane]:
            return person.hitbox.colliderect(self.sidewalk_lights[lane][0].hitbox) or person.hitbox.colliderect(self.sidewalk_lights[lane][1].hitbox)
        return 0

    def getNumberOfPeopleInSideWalk(self, people, position, lane=-1):
        if self.lane_exists[position]:
            people_hitboxes = []
            for person in people:
                people_hitboxes.append(person.hitbox)
            if lane == -1:
                return len(self.sidewalk_hitbox[position][0].collidelistall(people_hitboxes)) + \
                       len(self.sidewalk_hitbox[position][1].collidelistall(people_hitboxes))
            else:
                if lane == SOUTH:
                    lane = 1
                if lane == WEST or lane == EAST:
                    lane -= 1
                    return len(self.sidewalk_hitbox[position][lane].collidelistall(people_hitboxes))
        return 0

    def setSideWalkLight(self, position, light):
        if self.lane_exists[position]:
            self.sidewalk_lights[position][0].setLight(light)
            self.sidewalk_lights[position][1].setLight(light)

    def getSideWalkLight(self, position):
        if self.lane_exists[position]:
            return self.sidewalk_lights[position][0].getLight()
        return None

    def toggleSideWalkLight(self, position):
        if self.lane_exists[position]:
            if self.sidewalk_lights[position][0] == RED:
                self.setSideWalkLight(position, GREEN)
            else:
                self.setSideWalkLight(position, RED)

    def permuteSideWalkLight(self, position):
        if self.lane_exists[position]:
            self.sidewalk_lights[position][0].permute()
            self.sidewalk_lights[position][1].permute()