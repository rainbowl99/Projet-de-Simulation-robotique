from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 10
size_scene = (100, 70)
count = 0   # Count for creating different particules

univers = Univers("univers", size_scene, scale, 0.1)

force = Gravity(univers,g=V3D(0,9.81,0))
force.set_force()

viscosite = Viscosity(1, univers=univers)

# Initialization of the univers
univers.gameInit()
run = True  # run is to control the pygame and system
active = True   # active is to control the simulation continue/stop

instruction = ["Space: stop/continue", "Quit: quit", "Esc: add a random particule"]     # instruction for validation 2

while run:
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                univers.plot3D()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                active = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                count += 1
                name = "partiucle" + str(count)
                x = random() * size_scene[0] * scale
                y = random() * size_scene[1] * scale
                z = random() * scale ** 2

                vx = random() * scale ** 2
                vy = random() * scale ** 2
                vz = random() * scale ** 2
                r = random()
                g = random()
                b = random()
                rgb = (r, g, b, 1)

                p = Particule(name=name, color=rgb, masse=1, pos=V3D(x, y, z), vit=V3D(vx, vy, vz))
                univers.addAgent(p,reset=False)

        force.set_force()
        viscosite.set_force()

        univers.gameUpdate(active, instruction=instruction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
