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

        self.fraction_shirkers = None
        self.fraction_cooperators = None
        self.fraction_reciprocators = None

        self.smallest_group_size = None
        self.largest_group_size = None

        self.reporters = collections.OrderedDict.fromkeys(['n_agents', 'fraction_shirkers', 'fraction_cooperators',
                                                           'fraction_reciprocators', 'smallest_group_size', 'largest_group_size'])

    def calculate_population_distribution(self):
        """
        Calculate distribution of shirkers, cooperators and reciprocators in the population as a fraction of
        the total number of agents.
        :return:
        """
        counter = collections.Counter([a.type for a in self.agents])
        self.fraction_shirkers = counter["shirker"] / len(self.agents)
        self.fraction_cooperators = counter["cooperator"] / len(self.agents)
        self.fraction_reciprocators = counter["reciprocator"] / len(self.agents)

    def calculate_group_sizes(self):
        """
        Store size of smallest and largest group
        :return:
        """
        self.smallest_group_size = ABMtools.min_one_of(self.groups, 'size').size
        self.largest_group_size = ABMtools.max_one_of(self.groups, 'size').size


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
        if len(shirkers) > 0:
            self.shirking_rate = statistics.mean([a.shirking_decision for a in shirkers])
        else:
            self.shirking_rate = 0


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

        if self.group is None:
            return

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

                if self.shirking_decision > 1:
                    self.shirking_decision = 1
                if self.shirking_decision < 0:
                    self.shirking_decision = 0

    def calculate_fitness(self):
        """
        Calculate agent's fitness with appropriate formula based on agent's type. Sets agent's fitness property.
        :return:
        """
        if self.group is not None:
            own_group_fraction_shirkers = self.controller.group(self.group).fraction_shirkers
            own_group_shirking_rate = self.controller.group(self.group).shirking_rate
            cooperation_gain = self.controller.cooperation_gain
            cooperation_cost = self.controller.cooperation_cost
            punishing_cost = self.controller.punishing_cost

            if self.type == "shirker":
                self.fitness = (((1 - own_group_shirking_rate * own_group_fraction_shirkers) * cooperation_gain) -
                                ((1 - self.shirking_decision) ** 2 * cooperation_cost))
                # DEVIATION FROM NETLOGO MODEL WHERE self.shirking_decision IS REPLACED BY GROUP SHIRKING RATE
            elif self.type == "cooperator":
                self.fitness = (((1 - own_group_shirking_rate * own_group_fraction_shirkers) * cooperation_gain) -
                                cooperation_cost)
            elif self.type == "reciprocator":
                self.fitness = (((1 - own_group_shirking_rate * own_group_fraction_shirkers) * cooperation_gain) -
                                cooperation_cost - (punishing_cost * own_group_shirking_rate * own_group_fraction_shirkers))
        else:
            self.fitness = self.controller.fitness_in_pool


def setup():
    # Setup global variables by creating a controller with these properties
    c = Controller(initial_group_size=20, initial_num_groups=20, min_group_size=6, fitness_in_pool=-0.1,
                   initial_fraction_cooperators=0.2, initial_fraction_reciprocators=0.2, cooperation_cost=0.1,
                   punishing_cost=0.1, cooperation_gain=0.2, immigration_fraction=0.03, emigration_fraction=0.05,
                   mutation_rate=0.1)

    # Create agents
        # Create nr of agents equal to (c.initial-nr-of-groups * c.initial-size-of-groups)
        # Of these make sure the distribution is according to initial-fraction
        # All agents spawn with estimated ostracism cost randomly distributed [0,1)
        # All agents start not assigned to a group
    for _ in range(c.initial_group_size * c.initial_num_groups):
        c.create_agents(1, Agent, strategy_type='shirker', ostracism_estimate_cost=random.uniform(0, 1))
    number_cooperators = (100 * c.initial_fraction_cooperators) * (c.initial_group_size *  c.initial_num_groups) / 100
    number_reciprocators = (100 * c.initial_fraction_reciprocators) * (c.initial_group_size *  c.initial_num_groups) / 100
    agents_to_cooperators = random.sample([a for a in c.agents if a.type == "shirker"], int(number_cooperators))
    for a in agents_to_cooperators:
        a.type = "cooperator"
    agents_to_reciprocators = random.sample([a for a in c.agents if a.type == "shirker"], int(number_reciprocators))
    for a in agents_to_reciprocators:
        a.type = "reciprocator"


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
    #print(random.choice(c.groups).fraction_shirkers)

    # Decide shirking and calculate shirking rates
    for a in c.agents:
        a.decide_shirking()
    for g in c.groups:
        g.update_shirking_rate()

    #print([a.shirking_decision for a in c.agents])
    #print([g.shirking_rate for g in c.groups])


    # Calculate fitness
    for a in c.agents:
        a.calculate_fitness()

    # print([a.fitness for a in c.agents])

    # Reproduce
    for a in list(c.agents):
        if a.fitness < 0:
            if random.uniform(-1, 0) > a.fitness:
                #print("KILL {}".format(a.type))
                c.kill(a)
        if a.fitness > 0:
            if random.uniform(0, 1) < a.fitness:
                new_agent = a.hatch()
                #print("SPAWN {}".format(a.type))
                if random.uniform(0,1) < c.mutation_rate:
                    new_agent.type = random.choice(["shirker", "cooperator", "reciprocator"])
                    #print("MUTATE to {}".format(new_agent.type))

    # Ostracize
        # DIFFERENCE FROM NETLOGO IMPLEMENTATION: NO RECALCULATION OF RELEVANT GROUP VARIABLES
        # RATIONALE: Ostracism should happen based on same variables used to calculate shirking decisions and fitnesses
    for a in [a for a in c.agents if a.type == "shirker" and a.group is not None]:
        ostracism_probability = a.controller.group(a.group).fraction_reciprocators * a.shirking_decision
        if random.uniform(0, 1) < ostracism_probability:
            c.move(a, None)
            #print("OSTRACIZED to group {}".format(a.group))

    # Migrate
            # DIFFERENCE FROM NETLOGO IN THAT HERE I CONSTRUCT AN ACTUAL POOL OF MIGRATING AGENTS
            # CHECK IF PERHAPS THERE IS SOME MORE RANODMNESS IN ASSIGNMENT OF MIGRANTS TO GROUPS IN
            # ORIGINAL IMPLEMENTATION

    agents_in_pool = [a for a in c.agents if a.group is None]
    agents_in_groups = [a for a in c.agents if a.group is not None]
    num_agents_emigrating = int(c.emigration_fraction * len(agents_in_groups))
    migration_pool = agents_in_pool + random.sample(agents_in_groups, num_agents_emigrating)
    #print("SIZE OF MIGRATION POOL: {}".format(len(migration_pool)))

    immigrants_per_group = (c.immigration_fraction * len(agents_in_groups)) / c.initial_num_groups  # CHECK IF THIS SHOULD BE BASED ON GROUP SIZE?
    #print("IMMIGRANTS PER GROUP: {}".format(immigrants_per_group))
    for g in c.groups:
        immigrants_int = int(immigrants_per_group)
        immigrants_remainder = immigrants_per_group % 1

        for _ in range(immigrants_int):
            # If migration pool is empty don't attempt migration at all
            if len(migration_pool) < 1:
                break
            # IT IS CURRENTLY POSSIBLE FOR MIGRANTS TO MIGRATE TO THEIR OWN GROUP
            migrant = random.choice(migration_pool)
            #print("MIGRATING FROM GROUP {} TO GROUP {}".format(migrant.group, g.ident))
            c.move(migrant, g)
            migration_pool.remove(migrant)

        # If migration pool is empty don't attempt migration for this or any other group
        if len(migration_pool) < 1:
            break

        # Pick one last immigrant probabilistically, with chance equal to immigrants_remainder
        if random.uniform(0, 1) < immigrants_remainder:
            migrant = random.choice(migration_pool)
            #print("MIGRATING FROM GROUP {} TO GROUP {}".format(migrant.group, g.ident))
            c.move(migrant, g)
            migration_pool.remove(migrant)
    c.census()
    c.update_counts()

    # IF GENERATIONS GENERATIONS

    # Cull population if above starting total
    while c.n_agents > (c.initial_num_groups * c.initial_group_size):
        doomed_agent = random.choice(c.agents)
        #print("CULL {}".format(a.type))
        c.kill(doomed_agent)

    # Repopulate small groups
    for g in c.groups:
        if g.size < c.min_group_size:
            #print("CLEAR GROUP {}".format(g.ident))
            g.ungroup()

            for _ in range(c.initial_group_size):
                largest_group = ABMtools.max_one_of(c.groups, 'size')
                if largest_group.size > c.min_group_size:
                    #print("TAKE FROM GROUP {} OF SIZE {}".format(largest_group.ident, largest_group.size))
                    migrant = random.choice(largest_group.members)
                    c.move(migrant, g)
                elif len([a for a in c.agents if a.group is None]) > 0:
                    #print("TAKE FROM POOL")
                    pool = [a for a in c.agents if a.group is None]
                    migrant = random.choice(pool)
                    c.move(migrant, g)
                else:
                    print("TAKE FROM RANDOM GROUP")
                    pass

    c.census()
    c.update_counts()
    c.calculate_population_distribution()
    c.calculate_group_sizes()

    #print(c.n_agents)
    #print([g.size for g in c.groups])

if __name__ == "__main__":
    t = ABMtools.Ticker()
    t.set_setup(setup)
    t.setup()

    t.set_step(step, 1, t.controller)

    from datetime import datetime
    now = datetime.now()
    for _ in range(10000):
        t.step()
    then = datetime.now()
    diff = then - now
    print(diff)
