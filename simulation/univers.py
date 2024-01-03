# -*- coding: utf-8 -*-
import sys
import pygame
from matplotlib import pyplot as plt
from particule import Particule
from vecteur3D import Vecteur3D as V3D
import numpy as np


class Univers(object):
    def __init__(self, name, dimension, scale, step=0.1, background=(255, 255, 255)):
        self.active = True
        self.name = name
        self.step = step
        self.scale = scale
        self.dimension = np.array(dimension)
        self.time = 0  # Affiche Time on the screen(not the time of simulation), self.time = time of simulation - total paused time
        self.population = []
        self.generators = []
        self.background = background
        self.screen = None
        self.clock = pygame.time.Clock()
        self.timestamp = 0.0  # Timestamp for pause
        self.paused = False   # Continue/stop the simulation temporally
        self.paused_time_total = 0.0    # Save the total paused time in the simulation

    def getPopulation(self):
        return self.population

    def addAgent(self, *particule, reset=True):
        # Here this methode is seperated to two situations:
        # if reset is True, it means initializing the population in this univers
        # if reset is False, it means not initializing the population in this univers
        if reset:
            self.population = []
        self.population.extend(particule)
        return self.population

    def addSource(self, *generator):
        self.generators.extend(generator)

    def simule(self):
        for particule in self.population:
            particule.simule(self.step)

    def simuleAll(self, time):
        for particule in self.population:
            particule.simule(time)

    def gameInit(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.dimension * self.scale)
        pygame.display.set_caption(self.name)

    def gameUpdate(self, active=True, fps=60, instruction=None):
        self.active = active
        if self.active:
            if self.paused:
                self.paused_time_total = self.paused_time_total + pygame.time.get_ticks() / 1000.0 - self.timestamp     # save the paused time
                self.paused = False
            self.time = pygame.time.get_ticks() / 1000.0 - self.paused_time_total
            self.screen.fill(self.background)
            font = pygame.font.Font('freesansbold.ttf', 24)
            time_set = font.render(str(self.time)[:6], True, 'blue', self.background)

            text_rect_obj = time_set.get_rect()
            text_rect_obj.center = (25, 10)
            self.screen.blit(time_set, (50, 20))

            if instruction is not None:     # print the instruction for the program(line by line)
                count = 0
                row_interval = self.dimension[0] / 40 * self.scale
                for ele in instruction:
                    font1 = pygame.font.Font('freesansbold.ttf', 16)
                    instruction_set = font1.render(ele, True, 'red',
                                                   self.background)

                    text_rect_obj = instruction_set.get_rect()
                    text_rect_obj.center = (self.dimension[0] * self.scale * 0.8, 50)
                    self.screen.blit(instruction_set,
                                     (self.dimension[0] * self.scale * 0.75, 20 + row_interval * count))
                    count += 1

            self.simule()
            for particule in self.population:
                particule.gameDraw(self.screen)

            pygame.display.update()

            self.clock.tick(fps)    # fps = 60 by default

        elif not self.active and not self.paused:
            self.timestamp = pygame.time.get_ticks() / 1000.0
            self.paused = True      # Stop the simulation

    def plot2D(self):
        for particule in self.population:
            particule.plot2D()
        plt.show()

    def plot3D(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for particule in self.population:
            particule.plot3D(ax)
        ax.legend()
        plt.show()


if __name__ == "__main__":
    p1 = Particule("toto", "red", 1, vit=V3D(10, 10, 10))
    univers1 = Univers("univers1", (1080, 800), 1, 0.1)
    univers1.addAgent(p1)
    univers1.gameInit()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        univers1.gameUpdate()
    univers1.plot3D()
    pygame.quit()
    sys.exit()
