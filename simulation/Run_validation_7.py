from particule import Particule
from univers import Univers
from generator import *
from vecteur3D import Vecteur3D as V3D
from random import random
import pygame
import sys

scale = 1
size_scene = (1000, 700)
# timestamp = 0

univers = Univers("univers", size_scene, scale, 0.005)

r = random()
g = random()
b = random()
rgb1 = (r, g, b, 1)

p1_pos = V3D(500, 380, 0)
p1_vit = V3D()
p1_acc = V3D()
p1 = Particule(name="particule1", color=rgb1, masse=1, pos=p1_pos, vit=p1_vit, acc=p1_acc)

r = random()
g = random()
b = random()
rgb2 = (r, g, b, 1)

p2_pos = V3D(500, 320, 0)
p2_vit = V3D()
p2_acc = V3D()
p2 = Particule(name="particule2", color=rgb2, masse=1, pos=p2_pos, vit=p2_vit, acc=p2_acc)
univers.addAgent(p1, p2)

# save the initialization of position for p1 and p2

# create different forces
force = Gravity(univers, p2, g=V3D(0, 9.81, 0))
force.set_force()

axe = V3D(1, 0, 0)  # axe is for x-axis
speed = V3D(80, 0, 0)  # speed for commande clavier
force = V3D(10, 0, 0)  # force for auto control
prism = PrismJoint(axe=axe)

rod = Rod(p1, p2)


def game_draw(window, particule1, particule2):
    pygame.draw.line(window, particule2.color, (particule1.P[-1].x, particule1.P[-1].y),
                     (particule2.P[-1].x, particule2.P[-1].y))


univers.gameInit()
run = True
active = True
cb_clavier_run = False
cb_control_auto = False

instruction1 = ["Space: stop/continue", "Quit: quit", "Num 1: cb clavier", "Num 2: cb auto control"]
instruction2 = ["Left arrow: left", "Right arrow: right", "Esc: close cb clavier", "Quit: quit"]
instruction3 = ["Left arrow: force to the left", "Right arrow: force to the right", "Esc: close cb auto control",
                "Quit: quit"]

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
                cb_clavier_run = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                cb_control_auto = True
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            #     # Initialize the position
            #     p1 = Particule(name="particule1", color=rgb1, masse=1, pos=p1_pos, vit=p1_vit, acc=p1_acc)
            #     p2 = Particule(name="particule2", color=rgb2, masse=1, pos=p2_pos, vit=p2_vit, acc=p2_acc)
            #     univers.addAgent(p1, p2)
            #     # p1.P = [p1_pos]
            #     # p1.V = [p1_vit]
            #     # p1.A = [p1_acc]
            #     # p1.F = V3D()
            #     # p1.A_con = V3D()
            #     #
            #     # p2.P = [p2_pos]
            #     # p2.V = [p2_vit]
            #     # p2.A = [p2_acc]
            #     # p2.F = V3D()
            #     # p2.A_con = V3D()

        while cb_clavier_run:
            for EVENT in pygame.event.get():
                if EVENT.type == pygame.KEYDOWN and EVENT.key == pygame.K_LEFT:
                    p1.setSpeed(-speed)
                elif EVENT.type == pygame.KEYDOWN and EVENT.key == pygame.K_RIGHT:
                    p1.setSpeed(speed)
                elif EVENT.type == pygame.KEYDOWN and EVENT.key == pygame.K_ESCAPE:
                    cb_clavier_run = False
                # elif EVENT.type == pygame.KEYDOWN and EVENT.key == pygame.K_3:
                #     # Initialize the position
                #     p1 = Particule(name="particule1", color=rgb1, masse=1, pos=p1_pos, vit=p1_vit, acc=p1_acc)
                #     p2 = Particule(name="particule2", color=rgb2, masse=1, pos=p2_pos, vit=p2_vit, acc=p2_acc)
                #     univers.addAgent(p1, p2)
                #     # p1.P = [p1_pos]
                #     # p1.V = [p1_vit]
                #     # p1.A = [p1_acc]
                #     # p1.F = V3D()
                #     # p1.A_con = V3D()
                #     #
                #     # p2.P = [p2_pos]
                #     # p2.V = [p2_vit]
                #     # p2.A = [p2_acc]
                #     # p2.F = V3D()
                #     # p2.A_con = V3D()

                elif EVENT.type == pygame.QUIT:
                    pygame.quit()
                    univers.plot3D()
                    sys.exit()
                else:
                    p1.setSpeed(V3D())
            rod.set_force(p1, p2)
            game_draw(univers.screen, p1, p2)
            prism.set_force(particule=p1)
            pygame.display.update()

            univers.gameUpdate(active, fps=120, instruction=instruction2)

        while cb_control_auto:
            for Event in pygame.event.get():
                if Event.type == pygame.KEYDOWN and Event.key == pygame.K_LEFT:
                    p2.setSpeed(-force)
                elif Event.type == pygame.KEYDOWN and Event.key == pygame.K_RIGHT:
                    p2.setSpeed(force)
                elif Event.type == pygame.KEYDOWN and Event.key == pygame.K_ESCAPE:
                    cb_control_auto = False
                # elif Event.type == pygame.KEYDOWN and Event.key == pygame.K_3:
                #     # Initialize the position
                #     if timestamp == 0:
                #         timestamp = pygame.time.get_ticks() / 1000.0
                    # elif pygame.time.get_ticks() / 1000.0 - timestamp > 1e-4:
                    #     p1 = Particule(name="particule1", color=rgb1, masse=1, pos=p1_pos, vit=p1_vit, acc=p1_acc)
                    #     p2 = Particule(name="particule2", color=rgb2, masse=1, pos=p2_pos, vit=p2_vit, acc=p2_acc)
                    #     univers.addAgent(p1, p2)
                    #
                    #     # p1.P = [p1_pos,p1_pos]
                    #     # p1.V = [p1_vit]
                    #     # p1.A = [p1_acc]
                    #     # p1.F = V3D()
                    #     # p1.A_con = V3D()
                    #     #
                    #     # p2.P = [p2_pos,p2_pos]
                    #     # p2.V = [p2_vit]
                    #     # p2.A = [p2_acc]
                    #     # p2.F = V3D()
                    #     # p2.A_con = V3D()
                    #
                    #     prism.err_list = []
                    #     prism.err_somme = V3D()

                elif Event.type == pygame.QUIT:
                    pygame.quit()
                    univers.plot3D()
                    sys.exit()
                else:
                    p2.setSpeed(V3D())
                # timestamp = 0

            rod.set_force(p1, p2)
            prism.control_auto(particule1=p1, particule2=p2)
            prism.set_force(particule=p1)
            game_draw(univers.screen, p1, p2)
            pygame.display.update()

            univers.gameUpdate(active, fps=240, instruction=instruction3)

        rod.set_force(p1, p2)
        game_draw(univers.screen, p1, p2)
        prism.set_force(particule=p1)
        pygame.display.update()

        univers.gameUpdate(active, fps=240, instruction=instruction1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            univers.plot3D()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            active = True
