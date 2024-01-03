from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 100
size_scene = (10, 7)
centre = V3D(size_scene[0] / 2 * scale, size_scene[1] / 2 * scale, -5 * scale)

univers = Univers("univers", size_scene, scale, 0.1)
for t in range(10):
    name = 'Particule' + str(t)
    x = random() * size_scene[0] * scale
    y = random() * size_scene[1] * scale
    z = random() * scale * 100

    r = random()
    g = random()
    b = random()
    rgb = (r, g, b, 1)

    p = Particule(name=name, color=rgb, masse=1, pos=V3D(x, y, z))

    univers.addAgent(p,reset=False)

# Create the forces
force = Gravity(univers)
force.set_force()

force_field = ForceField(100, position=centre)

# Initialization of the univers
univers.gameInit()
run = True  # run is to control the pygame and system
active = True   # active is to control the simulation continue/stop

instruction = ["Space: stop/continue", "Quit: quit", "Esc: add a random particule"]

while run:
    while active:

        force_field.set_force(univers=univers)
        univers.gameUpdate(active,instruction=instruction)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                univers.plot3D()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Key space for controlling stop
                active = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
