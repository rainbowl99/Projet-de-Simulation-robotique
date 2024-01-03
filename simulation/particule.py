# -*- coding: utf-8 -*-
import pygame
from matplotlib import pyplot as plt
from vecteur3D import Vecteur3D as V3D


class Particule(object):
    def __init__(self, name, color, masse, fix=False, pos=None, vit=None, acc=None, force=None):
        self.name = name
        self.color = color
        self.M = masse
        self.fix = fix

        if pos is None:
            pos = V3D()
        if vit is None:
            vit = V3D()
        if acc is None:
            acc = V3D()
        if force is None:
            force = V3D()

        self.P = [pos]
        self.V = [vit]
        self.A_con = V3D()  # this is for set the constante acceleration for ex. gravity, it won't be considered in PFD but will be extra acceleration for particule
        self.A = [acc]  # The total acceleration of this particule is (self.A[-1]+self.A_con)
        self.F = force  # somme des forces

    def __str__(self):
        if self.fix:
            res = "fixed"
        else:
            res = "movable"

        return ("The " + res + f" {self.color} particule's name is {self.name}, and its masse is {self.M}. The "
                               f"initial speed is {self.V[0]} and the initial position is {self.P[0]}")

    def __repr__(self):
        return str(self)

    def PFD(self):
        # while self.fix is True, the acceleration of this particule is always (0,0,0)
        if self.fix:
            self.A.append(V3D())
            self.A_con = V3D()
        else:
            self.A.append(1 / self.M * self.F)

    def getPosition(self):
        return self.P[-1]

    def getSpeed(self):
        return self.V[-1]

    def simule(self, step):
        self.PFD()
        self.V.append(self.V[-1] + (self.A[-1] + self.A_con) * step)
        self.P.append(self.P[-1] + self.V[-1] * step + step ** 2 / 2.0 * (self.A[-1] + self.A_con))
        self.F = V3D()

    def setForce(self, force):
        if force is None:
            force = V3D()
        self.F += force

    def setSpeed(self, speed=None):
        if speed is None:
            speed = V3D()
        self.V.append(speed)

    def setPosition(self, position=None):
        if position is None:
            position = V3D()
        self.P.append(position)

    def plot2D(self):
        X = Y = []
        for p in self.P:
            X.append(p.x)
            Y.append(p.y)

        plt.figure(0)
        plt.plot(X, Y, color=self.color, label=self.name)
        plt.title("plot2D")
        plt.show()

    def plot3D(self, ax):
        X = []
        Y = []
        Z = []
        for p in self.P:
            X.append(p.x)
            Y.append(p.y)
            Z.append(p.z)

        ax.scatter(X, Y, Z, color=self.color, marker='o', label=self.name)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

    def gameDraw(self, window):
        X = self.P[-1].x
        Y = self.P[-1].y

        pygame.draw.circle(window, self.color, (X, Y), 4, 2)
