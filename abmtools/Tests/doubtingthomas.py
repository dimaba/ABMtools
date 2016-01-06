import random
import math
import statistics
from collections import OrderedDict
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import abmtools

class Controller(abmtools.Controller):
    def __init__(self, decayrate, efficiency, exit_chance, reporters):
        abmtools.Controller.__init__()
        self.decayrate = decayrate
        self.efficiency = efficiency
        self.exit_chance = exit_chance
        self.reporters = OrderedDict(reporters)
        self.average_quality_groups = None
        self.average_quality_enjoyed = None
        self.total_feedback = None
        self.percent_dissatisfied = None

    def calc_globals(self):
        self.average_quality_groups = statistics.mean([g.quality for g in self.groups])
        self.average_quality_enjoyed = math.fsum([g.quality * g.size for g in self.groups]) / len(self.agents)
        self.total_feedback = math.fsum([g.feedback for g in self.groups])
        self.percent_dissatisfied = len([a for a in self.agents if a.dissatisfied]) / len(self.agents)

class Group(abmtools.Group):
    def __init__(self, controller, quality=0):
        abmtools.Group.__init__(controller)
        self.quality = quality
        self.feedback = 0
        self.exiters = []

    def set_quality(self):
        self.feedback = self.calc_feedback()
        self.quality = (1 + self.feedback - self.controller.decayrate) * self.quality + self.feedback

    def calc_feedback(self):
        for a in self.members:
            a.set_feedback(self.quality)
            return self.controller.efficiency * math.fsum([a.feedback for a in self.members])

    def get_avg_threshold(self):
        if self.size == 0:
            return -1
        return statistics.mean([a.threshold for a in self.groupmembers])

class Actor(abmtools.Agent):
    def __init__(self, controller):
        abmtools.Agent.__init__(controller)
        self.threshold = 400 + random.randrange(-395, 395)
        self.feedback = 0
        self.dissatisfied = False
        self.exit = False

    def __str__(self):
        return "Actor with threshold {}".format(self.threshold)

    def set_feedback(self, quality):
        if quality < self.threshold:
            self.dissatisfied = True
            self.feedback = 1
            if random.random() <= self.controller.exit_chance:
                self.exit = True
            else:
                self.feedback = 1 / math.sqrt(1 + (quality - self.threshold)**2)

def setup(k=10):
    c = Controller()
    c.create_groups(k, Group)
    for g in c.groups:
        for i in range(20):
            c.create_agents(1, Actor, group=g.ident)
    c.census()
    return c

def step(c):
    for a in c.agents:
        a.dissatisfied = False
        a.exit = False

    for g in c.groups:
        g.set_quality()

    exiters = [a for a in c.agents if a.exit]
    for a in exiters:
        alternatives = [g for g in c.groups if g is not a.group]
        new = random.choice(alternatives)
        a.group = new

    c.census()

