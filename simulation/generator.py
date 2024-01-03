from vecteur3D import Vecteur3D as V3D
from math import cos


class Gravity(object):
    def __init__(self, univers, *particule, g=V3D(0, 0, -9.81)):
        self.g = g
        self.population = []
        # while no parameter particule, make the force apply on all the particules in the univers,
        # else add all particules in self.population
        if particule:
            self.population = []
            self.population.extend(particule)
        else:
            self.population = univers.population

    def set_force(self):
        for particule in self.population:
            # set constante acceleration but not calculate the forces
            particule.A_con = self.g


class ForceConst(object):
    def __init__(self, force=None):
        self.F = force if force is not None else V3D()
        self.population = []

    def set_force(self, univers, *particule):
        if not particule:
            self.population = []
            self.population = univers.population
        else:
            self.population.extend(particule)

        for particule in self.population:
            particule.setForce(self.F)


class ForceHarmonie(object):
    def __init__(self, pulsation, force=None):
        self.F = V3D()
        self.force = force if force is not None else V3D()
        self.pulsation = pulsation
        self.population = []

    def set_force(self, univers, *particule):
        if particule:
            self.population = []
            self.population.extend(particule)
        else:
            self.population = univers.population

        for particule in self.population:
            self.F = self.force * cos(self.pulsation * univers.time)
            particule.setForce(self.F)


class Viscosity(object):
    def __init__(self, coef, univers, *particule):
        self.coef = coef
        self.F = V3D()
        if not particule:
            self.population = univers.population
        else:
            self.population.extend(particule)

    def set_force(self):
        for particule in self.population:
            self.F = -self.coef * particule.V[-1]
            particule.setForce(self.F)


class ForceField(object):
    def __init__(self, amplitude, position=None):
        self.active = True
        self.amplitude = amplitude
        self.population = []

        self.F = 0
        if position is None:
            position = V3D()
        self.P = position

    def set_force(self, univers, *particule):
        if not particule:
            self.population = univers.population
        else:
            self.population.extend(particule)

        for element in self.population:
            direction = (element.P[-1] - self.P).norm()
            distance = (element.P[-1] - self.P).mod()
            self.F = -self.amplitude * 1 / distance * direction * element.M
            element.setForce(self.F)


class SpringDumper(object):
    def __init__(self, stiffness, dumping, length):
        self.active = True
        self.k = stiffness
        self.d = dumping
        self.len = length
        self.population = []

        self.dis = 0
        self.dis_vecteur = []
        self.dis_scalar = 0
        self.F = 0

    def set_force(self, particule1, particule2):
        self.dis = particule1.P[-1] - particule2.P[-1]
        self.dis_scalar = self.dis.mod()
        self.dis_vecteur = self.dis.norm()
        # The direction of the vector self.F is p2 to p1, so set self.F on p2 and -self.F on p1
        self.F = self.k * (self.dis_scalar - self.len) * self.dis_vecteur + self.d * (
                particule1.V[-1] - particule2.V[-1])
        particule2.setForce(self.F)
        particule1.setForce(-self.F)


class Rod(object):
    def __init__(self, particule1, particule2):
        self.k = 400  # Rod is for a ressort with a grand k and d = 0
        self.d = 0.0
        self.len = (particule1.P[-1] - particule2.P[-1]).mod()  # set the length automatically
        self.dis = V3D()
        self.dis_scalar = 0
        self.dis_vecteur = []
        self.F = V3D()

    def set_force(self, particule1, particule2):
        self.dis = particule1.P[-1] - particule2.P[-1]
        self.dis_scalar = self.dis.mod()
        self.dis_vecteur = self.dis.norm()
        # Same as SpringDumper
        self.F = self.k * (self.dis_scalar - self.len) * self.dis_vecteur + self.d * (
                particule1.V[-1] - particule2.V[-1])
        particule2.setForce(self.F)
        particule1.setForce(-self.F)


class PrismJoint(object):
    def __init__(self, axe):
        self.active = True
        if axe is None:
            axe = V3D(1, 0,
                      0)  # By default, 'axe' is used for the particle to slide along the x-axis. For y-axis: V3D(0,1,0)
        self.axe = axe
        self.err_list = []
        self.err_somme = V3D()

    def set_force(self, particule):
        # Projection on self.axe
        X = particule.F.x * self.axe.x
        Y = particule.F.y * self.axe.y
        Z = particule.F.z * self.axe.z
        particule.F = V3D(X, Y, Z)
        particule.A_con = V3D()

    def control_auto(self, particule1, particule2):
        kp = 10
        ki = 1
        kd = 0.03

        # PID control for inverse pendule
        err = particule2.P[-1] - particule2.P[-2]
        self.err_somme += err
        self.err_list.append(err)

        if len(self.err_list) == 1:
            print(err)
            F = kp * self.err_list[-1] + ki * self.err_somme
        else:
            F = kp * self.err_list[-1] + ki * self.err_somme + kd * (self.err_list[-1] - self.err_list[-2])

        # compare the x-axis position of particule1 and particule2 to make sure of applying the right direction force on particule1
        if (particule1.P[-1] - particule2.P[-1]).x > 0:
            particule1.setForce(-F)
            self.set_force(particule1)
        else:
            particule1.setForce(F)
            self.set_force(particule1)
