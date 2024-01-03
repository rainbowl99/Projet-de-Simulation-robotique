from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 10
size_scene = (100, 70)

univers = Univers("univers", size_scene, scale, 0.1)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)

p_left = Particule(name="particule_left", color=rgb, masse=1, fix=True, pos=V3D(35, 35, 0) * scale)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p_right = Particule(name="particule_right", color=rgb, masse=1, fix=True, pos=V3D(65, 35, 0) * scale)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p1 = Particule(name="particule1", color=rgb, masse=1, pos=V3D(45, 35, 0) * scale)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(55, 35, 0) * scale)

univers.addAgent(p_left, p_right, p1, p2)

ressort = SpringDumper(stiffness=10, dumping=0, length=10)


def game_draw(window, particule1, particule2):
    pygame.draw.line(window, particule2.color, (particule1.P[-1].x, particule1.P[-1].y),
                     (particule2.P[-1].x, particule2.P[-1].y))


# Initialization of the univers
univers.gameInit()
run = True  # run is to control the pygame and system
active = True   # active is to control the simulation continue/stop

instruction = ["Space: stop/continue", "Quit: quit", "Num 1: coherent vibration", "Num 2: counter-phase vibration", "Num 3: equilibrium position"]

while run:
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                univers.plot3D()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                active = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                univers.plot3D()    # Plot figure of previous movement
                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p1 = Particule(name="particule1", color=rgb, masse=1, pos=V3D(36, 35, 0) * scale)

                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(37, 35, 0) * scale)

                univers.addAgent(p_left, p_right, p1, p2)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                univers.plot3D()    # Plot figure of previous movement
                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p1 = Particule(name="particule1", color=rgb, masse=1, pos=V3D(36, 35, 0) * scale)

                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(64, 35, 0) * scale)

                univers.addAgent(p_left, p_right, p1, p2)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                univers.plot3D()    # Plot figure of previous movement
                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p1 = Particule(name="particule1", color=rgb, masse=1, pos=V3D(45, 35, 0) * scale)

                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)
                p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(55, 35, 0) * scale)

                univers.addAgent(p_left, p_right, p1, p2)

        ressort.set_force(p_left, p1)
        ressort.set_force(p1, p2)
        ressort.set_force(p2, p_right)

        game_draw(univers.screen, p_left, p1)
        game_draw(univers.screen, p1, p2)
        game_draw(univers.screen, p2, p_right)
        pygame.display.update()

        univers.gameUpdate(active, instruction=instruction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
