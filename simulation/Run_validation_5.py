from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 10
size_scene = (100, 70)
l0 = 15
l1 = 10

univers = Univers("univers", size_scene, scale, 0.01)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)

p1 = Particule(name="particule1", color=rgb, masse=1, fix=True, pos=V3D(50, 35, 0) * scale, vit=V3D(0, 0, 0))

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(50 + l0, 35, 0) * scale,
               vit=V3D(0, 0, 0))

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p3 = Particule(name="particule3", color=rgb, masse=1,pos=V3D(50 + l0, 35 - l1, 0) * scale, vit=V3D(0, 0, 0))

univers.addAgent(p1, p2, p3)

rod1 = Rod(p1, p2)
rod2 = Rod(p2, p3)
force = Gravity(univers, g=V3D(0, 9.81, 0))


def game_draw(window, particule1, particule2):
    pygame.draw.line(window, particule2.color, (particule1.P[-1].x, particule1.P[-1].y), (particule2.P[-1].x, particule2.P[-1].y))


# Initialization of the univers
univers.gameInit()
run = True  # run is to control the pygame and system
active = True   # active is to control the simulation continue/stop

instruction = ["Space: stop/continue", "Quit: quit"]

while run:
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                univers.plot3D()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                active = False

        force.set_force()
        rod1.set_force(p1, p2)
        game_draw(univers.screen, p1, p2)
        rod2.set_force(p2, p3)
        game_draw(univers.screen, p2, p3)
        pygame.display.update()

        univers.gameUpdate(active,fps=240,instruction=instruction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
