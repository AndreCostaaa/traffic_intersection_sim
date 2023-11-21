import os

import pygame

from Constants import WIDTH, HEIGHT, CIVILIAN_HEIGHT, CIVILIAN_WIDTH

SPORTS_CAR = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "SPORTS_CAR.png")), (128,64))
SPORTS_CAR_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "SPORTS_CAR1.png")), (128,64))
SPORTS_CAR_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "SPORTS_CAR2.png")), (128,64))
SPORTS_CAR_3 = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "SPORTS_CAR3.png")), (128,64))
SPORTS_CAR_ICONS = [SPORTS_CAR, SPORTS_CAR_1, SPORTS_CAR_2, SPORTS_CAR_3]

PERSON_1_LEFT = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "person_2_left.png")), (CIVILIAN_WIDTH,CIVILIAN_HEIGHT))
PERSON_1_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "person_2_right.png")), (CIVILIAN_WIDTH,CIVILIAN_HEIGHT))
PERSON_1_STANDING = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "person_2_standing.png")), (CIVILIAN_WIDTH,CIVILIAN_HEIGHT))
PERSON_1 = [PERSON_1_LEFT,PERSON_1_LEFT, PERSON_1_LEFT,PERSON_1_LEFT, PERSON_1_LEFT, PERSON_1_LEFT,
            PERSON_1_RIGHT, PERSON_1_RIGHT, PERSON_1_RIGHT, PERSON_1_RIGHT, PERSON_1_RIGHT, PERSON_1_RIGHT]

INFO_FONT = pygame.font.SysFont("comicsans",25)
