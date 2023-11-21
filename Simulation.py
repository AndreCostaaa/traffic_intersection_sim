import threading
import pygame
from Civilian import Civilian
from Constants import FPS, NORTH, EAST, WEST, RED, GREEN, YELLOW, EXIT, ENTRANCE, FREE_ZONE, BLACK, WIDTH, \
    UNDEF_POSITION, HORIZONTAL, VERTICAL, SOUTH, SET, GET, TRAFFIC_LIGHT, NEW, SIDE_WALK_LIGHT, CAR, CIVILIAN, \
    PERMUTE, CONNECTED, VERSION
from Media import INFO_FONT
from Physics import Physics
from SportsCar import SportsCar
from Main import connectToSerial, load_simulation
import random
from time import sleep
import sys
from Vehicle import Vehicle
from datetime import date


class Simulation:

    def __init__(self, win, terrain, serial, simulation_data):

        self.clock = pygame.time.Clock()
        self.window = win
        self.terrain = terrain
        self.collisions = 0
        self.run_overs = 0
        self.travel_time = []
        self.serial = serial
        self.start_time = pygame.time.get_ticks()
        self.CAR_SPAWN = pygame.USEREVENT + 0
        self.CIVILIAN_SPAWN = pygame.USEREVENT + 1
        self.SIMULATION_OVER = pygame.USEREVENT + 2
        if serial is not None:
            self.serial.open()
        if simulation_data is not None:
            self.simulation_data = simulation_data
            self.convertJsonData()
        self.spawn_index = 0

        self.set_command_dictionary = {TRAFFIC_LIGHT: self.terrain.setTrafficLight,
                                       SIDE_WALK_LIGHT: self.terrain.setSideWalkLight}
        self.get_command_dictionary = {TRAFFIC_LIGHT: self.terrain.getTrafficLight,
                                       SIDE_WALK_LIGHT: self.terrain.getSideWalkLight,
                                       CAR: self.terrain.getNumberOfCarsInLane,
                                       CIVILIAN: self.terrain.getNumberOfPeopleInSideWalk}
        self.permute_command_dictionary = {TRAFFIC_LIGHT: self.terrain.permuteTrafficLight,
                                           SIDE_WALK_LIGHT: self.terrain.permuteSideWalkLight}
        self.debug = False
        self.manual_control = False
        self.vehicle_list = []
        self.civilian_list = []
        self.draw_list = [self.terrain]
        self.queue_dict = {SportsCar: [self.carCanMove, self.vehicle_list],
                           Civilian: [self.personCanMove, self.civilian_list]}
        self.queue_list = []


        print()
        print("Welcome !")
        print("'F1' KeyBinds 'ESC' End Simulation")
        print()
        print("Refer to the user/developer guide for more info")
        print()
        print("Enjoy !")
        print()
        self.run()


    def run(self):
        old_keys = []
        run = True
        while run:
            delta_time = self.clock.get_time() / 1000
            self.clock.tick(FPS)

            # Inputs

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == self.CAR_SPAWN:
                    if self.simulation_data is not None:
                        self.spawnCar()
                        pygame.time.set_timer(self.CAR_SPAWN, int(self.simulation_data['car_spawn']['frequency']) * 1000)
                    else:
                        pygame.time.set_timer(self.CAR_SPAWN, 0)
                if event.type == self.CIVILIAN_SPAWN:
                    if self.simulation_data is not None:
                        self.spawnCivilianAtRandomLocation()
                        pygame.time.set_timer(self.CIVILIAN_SPAWN, int(self.simulation_data['civilian_spawn']['frequency']) * 1000)
                    else:
                        pygame.time.set_timer(self.CIVILIAN_SPAWN, 0)
                if event.type == self.SIMULATION_OVER:
                    pygame.time.set_timer(self.SIMULATION_OVER, 0)
                    pygame.time.set_timer(self.CAR_SPAWN, 0)
                    pygame.time.set_timer(self.CIVILIAN_SPAWN, 0)
            # Serial Communication
            if self.serial is not None:
                self.serial.getNewData()
                self.processIncomingData(self.serial.getData())

            # Keyboard
            keys = pygame.key.get_pressed()

            #Show Keybinds
            if keys[pygame.K_F1] and not old_keys[pygame.K_F1]:
                print("'F2' Manual Control - 'F10' To Setup Simulation - 'F11' To Setup Serial Communication - 'F12' Developer mode") 
            # Setup Serial Communication on another thread
            if keys[pygame.K_F11] and not old_keys[pygame.K_F11]:
                change_settings_thread = threading.Thread(target=self.setSerial)
                change_settings_thread.setDaemon(True)
                change_settings_thread.start()

            # Setup Simulation on another thread
            if keys[pygame.K_F10] and not old_keys[pygame.K_F10]:
                change_settings_thread = threading.Thread(target=self.setSimulation)
                change_settings_thread.setDaemon(True)
                change_settings_thread.start()

            # Manual Control
            if keys[pygame.K_F2] and not old_keys[pygame.K_F2]:
                self.manual_control = not self.manual_control
                if self.manual_control:
                    print()
                    print("Manual Control Mode")
                    print("Refer to your user/developer guide for keybinds")
                else:
                    print()
                    print("Exiting Manual Control Mode")

            # End Simulation
            if keys[pygame.K_ESCAPE]:
                self.print_results()
                run = False

            # Developer Mode
            if keys[pygame.K_F12] and not old_keys[pygame.K_F12]:
                self.debug = not self.debug

            if self.debug and keys[pygame.K_DELETE] and not old_keys[pygame.K_DELETE]:
                self.queue_list.clear()
                self.civilian_list.clear()
                Vehicle.number -= len(self.vehicle_list)
                self.vehicle_list.clear()
                self.draw_list.clear()
                self.draw_list.append(self.terrain)

            if self.manual_control:
                ini_pos = UNDEF_POSITION
                final_pos = UNDEF_POSITION
                if keys[pygame.K_q] and not old_keys[pygame.K_q]:
                    self.terrain.permuteTrafficLight(NORTH)
                if keys[pygame.K_w] and not old_keys[pygame.K_w]:
                    self.terrain.permuteTrafficLight(WEST)
                if keys[pygame.K_e] and not old_keys[pygame.K_e]:
                    self.terrain.permuteTrafficLight(EAST)
                if keys[pygame.K_r] and not old_keys[pygame.K_r]:
                    self.terrain.permuteTrafficLight(SOUTH)
                if keys[pygame.K_t] and not old_keys[pygame.K_t]:
                    self.terrain.permuteSideWalkLight(NORTH)
                if keys[pygame.K_y] and not old_keys[pygame.K_y]:
                    self.terrain.permuteSideWalkLight(WEST)
                if keys[pygame.K_u] and not old_keys[pygame.K_u]:
                    self.terrain.permuteSideWalkLight(EAST)
                if keys[pygame.K_i] and not old_keys[pygame.K_i]:
                    self.terrain.permuteSideWalkLight(SOUTH)
                if keys[pygame.K_SPACE]:
                    self.terrain.setTrafficLight(NORTH, RED)
                    self.terrain.setTrafficLight(WEST, RED)
                    self.terrain.setTrafficLight(EAST, RED)
                    self.terrain.setTrafficLight(SOUTH, RED)
                    self.terrain.setSideWalkLight(NORTH, RED)
                    self.terrain.setSideWalkLight(WEST, RED)
                    self.terrain.setSideWalkLight(EAST, RED)
                    self.terrain.setSideWalkLight(SOUTH, RED)
                if keys[pygame.K_a] and not old_keys[pygame.K_a]:
                    ini_pos = WEST
                    final_pos = NORTH
                if keys[pygame.K_s] and not old_keys[pygame.K_s]:
                    ini_pos = WEST
                    final_pos = EAST
                if keys[pygame.K_d] and not old_keys[pygame.K_d]:
                    ini_pos = WEST
                    final_pos = SOUTH
                if keys[pygame.K_f] and not old_keys[pygame.K_f]:
                    ini_pos = NORTH
                    final_pos = WEST
                if keys[pygame.K_g] and not old_keys[pygame.K_g]:
                    ini_pos = NORTH
                    final_pos = EAST
                if keys[pygame.K_h] and not old_keys[pygame.K_h]:
                    ini_pos = NORTH
                    final_pos = SOUTH
                if keys[pygame.K_j] and not old_keys[pygame.K_j]:
                    ini_pos = EAST
                    final_pos = NORTH
                if keys[pygame.K_k] and not old_keys[pygame.K_k]:
                    ini_pos = EAST
                    final_pos = WEST
                if keys[pygame.K_l] and not old_keys[pygame.K_l]:
                    ini_pos = EAST
                    final_pos = SOUTH
                if keys[pygame.K_v] and not old_keys[pygame.K_v]:
                    ini_pos = SOUTH
                    final_pos = NORTH
                if keys[pygame.K_b] and not old_keys[pygame.K_b]:
                    ini_pos = SOUTH
                    final_pos = WEST
                if keys[pygame.K_n] and not old_keys[pygame.K_n]:
                    ini_pos = SOUTH
                    final_pos = EAST
                if keys[pygame.K_p] and not old_keys[pygame.K_p]:
                    self.spawnCivilianAtRandomLocation()
                if ini_pos != UNDEF_POSITION and self.terrain.getCoordinates(ini_pos, final_pos) != UNDEF_POSITION:
                    self.queue_list.append(SportsCar(ini_pos, final_pos, self.terrain))

            if keys[pygame.K_F3] and not old_keys[pygame.K_F3]:
                print()
                print("Car at each road entrance")
                print(f"NORTH:{self.terrain.getNumberOfCarsInLane(NORTH, self.vehicle_list, ENTRANCE)} "
                      f"WEST:{self.terrain.getNumberOfCarsInLane(WEST, self.vehicle_list, ENTRANCE)} "
                      f"EAST:{self.terrain.getNumberOfCarsInLane(EAST, self.vehicle_list, ENTRANCE)} "
                      f"SOUTH:{self.terrain.getNumberOfCarsInLane(SOUTH, self.vehicle_list, ENTRANCE)}")
                print()
            if keys[pygame.K_F4] and not old_keys[pygame.K_F4]:
                print()
                print("Car at each road exit")
                print(f"NORTH:{self.terrain.getNumberOfCarsInLane(NORTH, self.vehicle_list, EXIT)} "
                      f"WEST:{self.terrain.getNumberOfCarsInLane(WEST, self.vehicle_list, EXIT)} "
                      f"EAST:{self.terrain.getNumberOfCarsInLane(EAST, self.vehicle_list, EXIT)} "
                      f"SOUTH:{self.terrain.getNumberOfCarsInLane(SOUTH, self.vehicle_list, EXIT)}")
                print()
            if keys[pygame.K_F5] and not old_keys[pygame.K_F5]:
                print()
                print("Car at each road")
                print(f"NORTH:{self.terrain.getNumberOfCarsInLane(NORTH, self.vehicle_list)} "
                      f"WEST:{self.terrain.getNumberOfCarsInLane(WEST, self.vehicle_list)} "
                      f"EAST:{self.terrain.getNumberOfCarsInLane(EAST, self.vehicle_list)} "
                      f"SOUTH:{self.terrain.getNumberOfCarsInLane(SOUTH, self.vehicle_list)} "
                      f"MIDDLE:{self.terrain.getNumberOfCarsInLane(FREE_ZONE, self.vehicle_list)}")
                print()
            if keys[pygame.K_F6] and not old_keys[pygame.K_F6]:
                print()
                print("Civilians at each sidewalk")
                print(f"NW:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, NORTH, WEST)} "
                      f"NE:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, NORTH, EAST)} "
                      f"EN:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, EAST, NORTH)} "
                      f"ES:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, EAST, SOUTH)} "
                      f"WN:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, WEST, NORTH)} "
                      f"WS:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, WEST, SOUTH)} "
                      f"SW:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, SOUTH, WEST)} "
                      f"SE:{self.terrain.getNumberOfPeopleInSideWalk(self.civilian_list, SOUTH, EAST)}")
                print()
            old_keys = keys
            # Compute
            # Queue List
            for index, ele in sorted(enumerate(self.queue_list), reverse=True):
                if self.addFromQueue(ele):
                    self.queue_list.remove(ele)

            # Car list
            pop_list = []
            to_break = False
            for car in self.vehicle_list:
                for pop in pop_list:
                    if pop is car:
                        to_break = True
                if to_break:
                    break
                # get car lane
                lane = self.terrain.getLane(car)
                # check if it is out of the screen
                if car.isOutOfScreen():
                    self.travel_time.append((pygame.time.get_ticks() - car.getStartTime()) / 1000)
                    pop_list.append(car)
                    break
                if lane[1] == EXIT:
                    car.velocity.x = 7
                    car.move(delta_time)
                elif lane[1] == ENTRANCE:
                    if self.terrain.getInTrafficLight(car):
                        light = self.terrain.getTrafficLight(lane[0])
                        if light == RED:
                            car.stop()
                        elif light == YELLOW:
                            car.stop()
                        elif light == GREEN:
                            car.go()
                    if self.carCanMove(car, car.getHitboxPreview(delta_time)):
                        car.move(delta_time)
                elif lane[1] == FREE_ZONE:
                    car.move(delta_time)
                    lst = self.getCollisions(car)
                    for obj in lst:
                        pop_list.append(obj)
                else:
                    print("Error 1")
                    Vehicle.number -= 1
                    pop_list.append(car)
                    break

            # converting the list to a set and back to a list so i don't have the same object twice inside the list
            pop_list = set(pop_list)
            pop_list = list(pop_list)
            for pop in pop_list:
                self.draw_list.remove(pop)
                if type(pop) == SportsCar:
                    self.vehicle_list.remove(pop)
                elif type(pop) == Civilian:
                    self.civilian_list.remove(pop)

            # civilian list
            for index, person in sorted(enumerate(self.civilian_list), reverse=True):
                side_walk = self.terrain.getSideWalk(person)
                if person.isOutOfScreen():
                    self.civilian_list.remove(person)
                    self.draw_list.remove(person)
                    break
                if self.terrain.getInSideWalkLight(person, side_walk[0]) and not person.crossing:
                    if not person.changed_direction:
                        person.changeDirection(side_walk[1])
                    if self.terrain.getSideWalkLight(side_walk[0]) == RED:
                        person.stop()
                    elif self.terrain.getSideWalkLight(side_walk[0]) == YELLOW:
                        person.stop()
                    elif self.terrain.getSideWalkLight(side_walk[0]) == GREEN:
                        person.go(side_walk[1])
                        person.crossing = True
                if self.personCanMove(person):
                    person.move()
                else:
                    person.setStanding()

            self.draw(self.draw_list)

    def draw(self, draw_list):
        for obj in draw_list:
            obj.draw(self.window, self.debug)
        
        y = 0

        # collisions
        total_nb_cars_text = INFO_FONT.render(f"Total Number Of Cars: {Vehicle.number:>6}", 1, BLACK)
        collisions_text = INFO_FONT.render(f"Collisions: {self.collisions:>6}", 1, BLACK)
        cars_crossed_text = INFO_FONT.render(f"Cars Crossed: {len(self.travel_time):>6}", 1, BLACK)
        if len(self.travel_time) > 0:
            percentage_crossed_text = INFO_FONT.render(f"% Of Cars Crossed: {len(self.travel_time) / Vehicle.number * 100:>6.2f} %", 1, BLACK)
        else:
            percentage_crossed_text = INFO_FONT.render( f"% Of Cars Crossed: {len(self.travel_time):>6.2f} %", 1, BLACK)
        total_nb_ppl_text = INFO_FONT.render(f"Total Number Of People: {Civilian.number:>6}", 1, BLACK)
        run_overs_text = INFO_FONT.render(f"Run Overs: {self.run_overs:>6}", 1, BLACK)
        if Civilian.number > 0:
            mortality_rate_text = INFO_FONT.render(f"Mortality Rate: {self.run_overs / Civilian.number * 100:>6.2f} %", 1, BLACK)
        else:
            mortality_rate_text = INFO_FONT.render(f"Mortality Rate: {Civilian.number:>6.2f} %", 1, BLACK)

        self.window.blit(total_nb_cars_text, (WIDTH - total_nb_cars_text.get_width() - 10, y))
        y += total_nb_cars_text.get_height() + 5
        self.window.blit(cars_crossed_text, (WIDTH - cars_crossed_text.get_width() - 10, y))
        y += cars_crossed_text.get_height() + 5
        self.window.blit(collisions_text, (WIDTH - collisions_text.get_width() - 10, y))
        y += collisions_text.get_height() + 5
        self.window.blit(percentage_crossed_text, (WIDTH - percentage_crossed_text.get_width() - 10, y))
        y += percentage_crossed_text.get_height() + 5

        y += 20
        self.window.blit(total_nb_ppl_text, (WIDTH - total_nb_ppl_text.get_width() - 10, y))
        y += total_nb_ppl_text.get_height() + 5
        self.window.blit(run_overs_text, (WIDTH - run_overs_text.get_width() - 10, y))
        y += run_overs_text.get_height() + 5
        self.window.blit(mortality_rate_text, (WIDTH - mortality_rate_text.get_width() - 10, y))
        y += mortality_rate_text.get_height() + 5

        # travel times
        if len(self.travel_time) > 0:
            avg_travel_time = 0
            max_travel_time = self.travel_time[0]
            min_travel_time = self.travel_time[0]

            for i in self.travel_time:
                avg_travel_time += i
                max_travel_time = max(max_travel_time, i)
                min_travel_time = min(min_travel_time, i)
            avg_travel_time /= len(self.travel_time)
            y += 20
            avg_travel_time_text = INFO_FONT.render(f"Average Travel Time: {avg_travel_time:>6.2f} seconds", 1, BLACK)
            min_travel_time_text = INFO_FONT.render(f"Minimum Travel Time: {min_travel_time:>6.2f} seconds", 1, BLACK)
            max_travel_time_text = INFO_FONT.render(f"Maximum Travel Time: {max_travel_time:>6.2f} seconds", 1, BLACK)

            self.window.blit(avg_travel_time_text, (WIDTH - avg_travel_time_text.get_width() - 10, y))
            y += avg_travel_time_text.get_height() + 5
            self.window.blit(min_travel_time_text, (WIDTH - min_travel_time_text.get_width() - 10, y))
            y += min_travel_time_text.get_height() + 5
            self.window.blit(max_travel_time_text, (WIDTH - max_travel_time_text.get_width() - 10, y))
            y += max_travel_time_text.get_height() + 5
        pygame.display.update()

    def getCollisions(self, car):
        pop = []
        for i, v in sorted(enumerate(self.vehicle_list), reverse=False):
            if v is not car:
                if Physics.collide(car, v):
                    if Physics.hitboxes_collide(v.hitbox, car.hitbox):
                        if v.ini_pos != car.ini_pos:
                            pop.append(car)
                            pop.append(v)
                            self.collisions += 1
                            break
                        else:
                            pass
                            #getting the two cars that collided
                            '''car_to_slow_down = self.vehicle_list[max(i, self.vehicle_list.index(car))]
                            other = self.vehicle_list[min(i, self.vehicle_list.index(car))]
                            #instead of slowing down the car that's behind, i figured out that speeding up the car that is in front works better
                          other.velocity.x = car_to_slow_down.velocity.x + 0.5'''
                else:
                    car.velocity = car.default_velocity
        for i, p in sorted(enumerate(self.civilian_list), reverse=False):
            if Physics.hitboxes_collide(car.hitbox, p.hitbox):
                pop.append(p)
                self.run_overs += 1
        pop = set(pop)
        pop = list(pop)
        return pop

    def addFromQueue(self, obj):
        # Queue dict receives the type of the obj and gives us the function at index 0
        # and the list of the same type of objects at index 1
        funct = self.queue_dict[type(obj)][0]
        lst = self.queue_dict[type(obj)][1]
        if funct(obj):
            lst.append(obj)
            self.draw_list.append(obj)
            return True
        return False

    def carCanMove(self, car, car_preview_hitbox=UNDEF_POSITION):
        if car_preview_hitbox == UNDEF_POSITION:
            for c in self.vehicle_list:
                if c is not car:
                    if Physics.hitboxes_collide(c.hitbox, car.hitbox):
                        return False
            return True
        else:
            for c in self.vehicle_list:
                if c is not car:
                    if Physics.hitboxes_collide(c.hitbox, car_preview_hitbox):
                        return False
            return True

    def personCanMove(self, person):
        for p in self.civilian_list:
            if p is person:
                break
            if Physics.hitboxes_collide(person.getHitboxPreview(), p.hitbox):
                return False
        for v in self.vehicle_list:
            if Physics.hitboxes_collide(person.getHitboxPreview(), v.hitbox):
                return False
        return True

    def processIncomingData(self, data):
        if data:
            try:
                if data[0] == SET:
                    func = self.set_command_dictionary[data[1]]
                    func(int(data[2]), data[3])

                elif data[0] == GET:
                    func = self.get_command_dictionary[data[1]]
                    if data[1] == CAR:
                        try:
                            self.serial.setData(str(func(int(data[2]), self.vehicle_list, int(data[3]))) + '\n')
                        except:
                            self.serial.setData(str(func(int(data[2]), self.vehicle_list)) + '\n')
                    elif data[1] == CIVILIAN:
                        try:
                            self.serial.setData(str(func(self.civilian_list, int(data[2]), int(data[3]))) + '\n')
                        except:
                            self.serial.setData(str(func(self.civilian_list, int(data[2]))) + '\n')
                    else:  # traffic lights
                        self.serial.setData(str(func(int(data[2])) + '\n'))

                elif data[0] == NEW:
                    if data[1] == CAR:
                        self.queue_list.append(SportsCar(int(data[2]), int(data[3]), self.terrain))
                    elif data[1] == CIVILIAN:
                        self.spawnCivilianAtRandomLocation()

                elif data[0] == PERMUTE:
                    func = self.permute_command_dictionary[data[1]]
                    func(int(data[2]))
            except:
                self.invalidData(data)

    def invalidData(self, data):
        print("Invalid data" + str(data))

    def spawnCivilianAtRandomLocation(self):

        spawn = [random.randint(NORTH, SOUTH), random.randint(NORTH, SOUTH)]
        if spawn[0] == NORTH:
            direction = VERTICAL
            speed = 4
        elif spawn[0] == WEST:
            direction = HORIZONTAL
            speed = 4
        elif spawn[0] == EAST:
            direction = HORIZONTAL
            speed = -4
        elif spawn[0] == SOUTH:
            direction = VERTICAL
            speed = -4
        pos = self.terrain.getSideWalkSpawnCoordinates(spawn)
        if pos != UNDEF_POSITION:
            self.queue_list.append(Civilian(pos, direction, speed))

    def spawnCar(self):
        if self.simulation_data['car_spawn']['random_routes']:
            spawned = False
            while not spawned:
                start_pos = random.randint(NORTH, SOUTH)
                final_pos = random.randint(NORTH, SOUTH)
                if self.terrain.getCoordinates(start_pos, final_pos) != UNDEF_POSITION and start_pos != final_pos:
                    self.queue_list.append(SportsCar(start_pos, final_pos, self.terrain))
                    spawned = True
        else:
            start_pos = self.simulation_data['car_spawn']['routes'][self.spawn_index][0]
            final_pos = self.simulation_data['car_spawn']['routes'][self.spawn_index][1]

            if self.terrain.getCoordinates(start_pos, final_pos) != UNDEF_POSITION:
                self.queue_list.append(SportsCar(start_pos, final_pos, self.terrain))
            self.spawn_index += 1
            if self.spawn_index >= len(self.simulation_data['car_spawn']['routes']):
                self.spawn_index = 0

    def convertJsonData(self):
        pygame.time.set_timer(self.CAR_SPAWN, int(self.simulation_data['car_spawn']['frequency']) * 1000)
        pygame.time.set_timer(self.CIVILIAN_SPAWN, int(self.simulation_data['civilian_spawn']['frequency']) * 1000)
        pygame.time.set_timer(self.SIMULATION_OVER, int(self.simulation_data['simulation_time']) * 1000) 
        if not self.simulation_data['car_spawn']['random_routes']:
            for i in range(len(self.simulation_data['car_spawn']['routes'])):
                for j in range(2):
                    if 'n' in self.simulation_data['car_spawn']['routes'][i][j]:
                        self.simulation_data['car_spawn']['routes'][i][j] = NORTH

                    elif 'w' in self.simulation_data['car_spawn']['routes'][i][j]:
                        self.simulation_data['car_spawn']['routes'][i][j] = WEST

                    elif 'e' in self.simulation_data['car_spawn']['routes'][i][j]:
                        self.simulation_data['car_spawn']['routes'][i][j] = EAST

                    elif 's' in self.simulation_data['car_spawn']['routes'][i][j]:
                        self.simulation_data['car_spawn']['routes'][i][j] = SOUTH
        print("Simulation loaded")

    def print_results(self):
        print("------------- RESULTS OF THE SIMULATION -------------")
        print("\nTraffic Intersection Simulator " + VERSION + " " + str(date.today()))
        print("\nSimulation Time: " + str((pygame.time.get_ticks() - self.start_time) / 1000) + " seconds")
        if(Vehicle.number > 0):
            print("\nNumber of Cars Spawned: " + str(Vehicle.number))
            print("Number of Cars Crossed: " + str(len(self.travel_time)))
            print("Number of Collisions: " + str(self.collisions))
            print(f"Cars Crossed: {(len(self.travel_time) / Vehicle.number * 100):>6.2f}%")
        if(Civilian.number > 0):
            print("\nNumber of Civilians: "+ str(Civilian.number))
            print("Number of Run Overs: " + str(self.run_overs))
            print(f"Mortality Rate: {(self.run_overs / Civilian.number * 100):>6.2f}%")
                # travel times
        if len(self.travel_time) > 0:
            avg_travel_time = 0
            max_travel_time = self.travel_time[0]
            min_travel_time = self.travel_time[0]

            for i in self.travel_time:
                avg_travel_time += i
                max_travel_time = max(max_travel_time, i)
                min_travel_time = min(min_travel_time, i)
            avg_travel_time /= len(self.travel_time)
            print(f"\nAverage Travel Time: {avg_travel_time:>7.2f} seconds")
            print(f"Minimum Travel Time: {min_travel_time:>7.2f} seconds")
            print(f"Maximum Travel Time: {max_travel_time:>7.2f} seconds")
        print("-----------------------------------------------------")

    # Threads functions
    def setSerial(self):
        inp = input("Setup a New Serial Communication [Y]es [N]o? ")
        if 'y' in inp.lower():
            if self.serial is not None:
                self.serial.close()
                sleep(0.25)
            self.serial = connectToSerial()
            if self.serial is not None:
                self.serial.open()

    def setSimulation(self):
        inp = input("Load a New Simulation File [Y]es [N]o? ")
        if 'y' in inp.lower():
            self.simulation_data = load_simulation()
            if self.simulation_data is not None:
                self.convertJsonData()
            else:
                print("Simulation Data not Found")