import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import ABMtools
import random
import collections
import statistics

"""
Three types of agents:
    1. cooperators
    2. shirkers
    3. reciprocators

They are all agents but are distinguished by different behavior.
"""

class Controller(ABMtools.Controller):
    """
    Controller:
        Properties: initial size of groups, initial number of groups, minimum group size,
        fitness for agents outside of any group, initial fraction cooperators, initial fraction reciprocators
        Reporters for: mean fitness of shirkers, mean fitness of reciprocators, mean fitness of cooperators,
        mean fitness of all agents
    """
    def __init__(self, initial_group_size, initial_num_groups, min_group_size, fitness_in_pool,
                 initial_fraction_cooperators, initial_fraction_reciprocators, cooperation_cost,
                 punishing_cost, cooperation_gain, immigration_fraction, emigration_fraction, mutation_rate,
                 *args, **kwargs):
        ABMtools.Controller.__init__(self, *args, **kwargs)
        self.initial_group_size = initial_group_size
        self.initial_num_groups = initial_num_groups
        self.min_group_size = min_group_size
        self.fitness_in_pool = fitness_in_pool
        self.initial_fraction_cooperators = initial_fraction_cooperators
        self.initial_fraction_reciprocators = initial_fraction_reciprocators
        self.cooperation_cost = cooperation_cost
        self.punishing_cost = punishing_cost
        self.cooperation_gain = cooperation_gain
        self.immigration_fraction = immigration_fraction
        self.emigration_fraction = emigration_fraction
        self.mutation_rate = mutation_rate


class Group(ABMtools.Group):
    """
    Prototype group:
        Properties: group size
        Reporter values or functions: group shirking rate, group size, group fraction reciprocators,
        group fraction shirkers, fitness for shirkers in group, fitness for reciprocators in group, fitness for
        cooperators in group
        group-size-at-shirking? group-fr-at-shirking? group-fs-at-shirking?
    """
    def __init__(self, *args, **kwargs):
        ABMtools.Group.__init__(self, *args, **kwargs)
        self.fraction_shirkers = None
        self.fraction_cooperators = None
        self.fraction_reciprocators = None
        self.shirking_rate = None

    def update_population_distribution(self):
        """
        Get counts of agents for each type, calculate fractions of agents for each type and store fractions
        :return:
        """
        counter = collections.Counter([a.type for a in self.members])
        self.fraction_shirkers = counter['shirker'] / self.size
        self.fraction_cooperators = counter['cooperator'] / self.size
        self.fraction_reciprocators = counter['reciprocator'] / self.size

    def update_shirking_rate(self):
        """
        Calculate average shirking rate across all group members who are shirkers

        :return:
        """
        shirkers = [a for a in self.members if a.type == "shirker"]
        self.shirking_rate = statistics.mean([a.shirking_decision for a in shirkers])

class Agent(ABMtools.Agent):
    """
    Prototype agent:
        Properties: type (c,s,r) estimated loss from ostracism, fitness, age, shirking decision
    """
    def __init__(self, controller, strategy_type, ostracism_estimate_cost, fitness=None, age=None, shirking_decision=None, *args, **kwargs):
        ABMtools.Agent.__init__(self, controller, *args, **kwargs)
        self.type = strategy_type
        self.ostracism_estimate_cost = ostracism_estimate_cost
        self.fitness = fitness
        self.age = age
        self.shirking_decision = shirking_decision

    def decide_shirking(self):
        """
        Decide appropriate shirking rate for this agent based on agent's type, agent group's size and fraction of
        reciprocators, taking into account this agent's estimated cost from potential ostracism

        :return:
        """
        if self.type in ["cooperator", "reciprocator"]:
            self.shirking_decision = 0


        if self.type == "shirker":
            own_group = self.controller.group(self.group)
            # Maximum acceptable percentage of reciprocators in the group to shirk at all
            fr_max = ((2 * self.controller.cooperation_cost + (self.controller.cooperation_gain /
                                                               own_group.size)) /
                      self.ostracism_estimate_cost)

            if own_group.fraction_reciprocators > fr_max:
                self.shirking_decision = 0
            else:
                self.shirking_decision = (1 - (own_group.fraction_reciprocators * self.ostracism_estimate_cost *
                                          own_group.size - self.controller.cooperation_gain) / (2 * self.controller.cooperation_cost * own_group.size))
                #print("(1 - ({} * {} * {} - {}) / (2 * {} * {}))".format(own_group.fraction_reciprocators, self.ostracism_estimate_cost, own_group.size,
                #                                                      self.controller.cooperation_gain, self.controller.cooperation_cost, own_group.size))
                # formula page 5 bowles/gintis adapted by A. (+ b instead of - b)
                # how the paper describes shirking decisions, but adapted ->
                # it's possible for this to return a sigma below 0 for large FR/large S
                #assert 0 <= self.shirking_decision <= 1


def setup():
    # Setup global variables by creating a controller with these properties
    c = Controller(initial_group_size=20, initial_num_groups=20, min_group_size=6, fitness_in_pool=-0.1,
                   initial_fraction_cooperators=0, initial_fraction_reciprocators=0, cooperation_cost=0.1,
                   punishing_cost=0.1, cooperation_gain=0.2, immigration_fraction=0.03, emigration_fraction=0.05,
                   mutation_rate=0.01)

    # Create agents
        # Create nr of agents equal to (c.initial-nr-of-groups * c.initial-size-of-groups)
        # Of these make sure the distribution is according to initial-fraction
        # All agents spawn with estimated ostracism cost randomly distributed [0,1)
        # All agents start not assigned to a group
    for _ in range(c.initial_group_size * c.initial_num_groups):
        c.create_agents(1, Agent, strategy_type='shirker', ostracism_estimate_cost=random.uniform(0, 1))

        # STARTING WITH NO COOPERATORS AND RECIPROCATORS ATM

    # Create groups
        # Create nr of groups equal to c.initial-nr-of-groups
        # Pick c.initial-size-of-groups from agents who don't have a group yet
    c.create_groups(c.initial_num_groups, Group)
    agents_without_group = list(c.agents)

    for g in c.groups:
        for _ in range(c.initial_group_size):
            agent = random.choice(agents_without_group)
            agent.group = g.ident
            agents_without_group.remove(agent)

    c.census()

    #for g in c.groups:
    #    print(g.ident, g.size, [str(a) for a in g.members])

    return c


def step(i, c):
    # Update group level variables
    for g in c.groups:
        g.update_population_distribution()
    print(random.choice(c.groups).fraction_shirkers)

    # Decide shirking and calculate shirking rates
    for a in c.agents:
        a.decide_shirking()
    for g in c.groups:
        g.update_shirking_rate()

    print([a.shirking_decision for a in c.agents])
    print([g.shirking_rate for g in c.groups])


    # Calculate fitness

    # Reproduce

    # Ostracize

    # Migrate

    # IF GENERATIONS GENERATIONS

    # Cull population

    # Repopulate small groups


if __name__ == "__main__":
    c = setup()
    step(1, c)
