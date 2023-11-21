import pygame
import sys
import os
import json
from Constants import WIDTH, HEIGHT, CONNECTED
from time import sleep

def connectToSerial():

    from SerialCommunication import Serial
    serial = None
    br_is_int = False
    if 'y' in input("Set up Serial COM [Y]es [N]o :").lower():
        com = input("Select Serial COM: ")
        com = 'COM' + com
        baud_rate = input("Select BaudRate: ")
        while not br_is_int:
            try:
                baud_rate = int(baud_rate)
                br_is_int = True
            except:
                print('........................')
                print("Baudrate must be an integer")
                baud_rate = input("Select BaudRate: ")
        try:
            serial = Serial(com, baud_rate, 1)
            print('........................')
            print("Successful Connection")
        except:
            print('........................')
            print("Unsuccessful Connection")
    if serial is not None:
        sleep(1)
        serial.setData(CONNECTED)
    return serial


def load_simulation():
    if 'y' in input("Load Simulation [Y]es [N]o? ").lower():
        simulation = os.path.join('assets\sim', 'Simulation' + input("Simulation number:") + '.json')
        try:
            with open(simulation) as r:
                return json.load(r)
        except:
            print("Simulation load failed")
            print("Does the file " + str(simulation) + " exist?")
    return None

def main():
    pygame.font.init()
    from Map import Map
    from Simulation import Simulation
    while True:
        map_name = input("Enter Map Name or 'quit' to quit: ")
        if 'quit' in map_name or 'exit' in map_name:
            sys.exit()
        serial = connectToSerial()
        simulation_data = load_simulation()
        pygame.init()
        pygame.display.set_caption("Traffic Intersection Simulator")
        window = pygame.display.set_mode((WIDTH, HEIGHT))

        Simulation(window, Map(map_name), serial, simulation_data)

        pygame.display.quit()

if __name__ == '__main__':
    main()