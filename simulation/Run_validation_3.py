from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 1
size_scene = (1000, 700)

univers = Univers("univers", size_scene, scale, 0.1)

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)

p1 = Particule(name="particule1", color=rgb, masse=1, fix=True, pos=V3D(350, 350, 0), vit=V3D(0, 0, 0))

r = random()
g = random()
b = random()
rgb = (r, g, b, 1)
p2 = Particule(name="particule2", color=rgb, masse=1, pos=V3D(650, 350, 0), vit=V3D(0, 0, 0))
univers.addAgent(p1, p2)

# Create all forces
force_const = ForceConst(force=V3D(1000, 0, 0))
force_harmonique = ForceHarmonie(pulsation=2, force=V3D(1000, 0, 0))
RA = SpringDumper(stiffness=10, dumping=0.1, length=400)


def game_draw(window, particule1, particule2):
    pygame.draw.line(window, particule2.color, (particule1.P[-1].x, particule1.P[-1].y), (particule2.P[-1].x, particule2.P[-1].y))
    pygame.display.update()


# Initialization of the univers
univers.gameInit()
run = True  # run is to control the pygame and system
active = True   # active is to control the simulation continue/stop
key = 0     # Key for applying different forces

instruction = ["Space: stop/continue", "Quit: quit", "Num 1: apply constance force", "Num 2: apply harmonie force", "Num 3: delete all forces applied"]

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
                key = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                key = 2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                key = 0

        if key == 1:
            force_const.set_force(univers=univers)
        elif key == 2:
            force_harmonique.set_force(univers, p2)

        RA.set_force(p1, p2)
        game_draw(univers.screen, p1, p2)

        univers.gameUpdate(active, fps=120, instruction=instruction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
