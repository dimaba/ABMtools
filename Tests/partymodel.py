# EXAMPLE MODEL : COPY OF NETLOGO 'PARTY' MODEL
import ABMtools
import random
import sys

class Party(ABMtools.Controller):
    # Parties have the following attributes:
    # 1. Total number present, 2. Number of groups in which they are split,
    # 3. Tolerance for other-sex in %, 4. Number of boring (single-sex) groups
    def __init__(self, n, k, tolerance, *args, **kwargs):
        ABMtools.Controller.__init__(self, *args, **kwargs)
        self.n = n
        self.k = k
        self.tolerance = tolerance
        self.boringgroups = 0

    def count_boring(self):
        bg = 0
        for g in self.groups:
            if all([a.sex == "M" for a in g.members]) or all([a.sex == "F" for a in g.members]):
                bg += 1
        self.boringgroups = bg

class Partier(ABMtools.Agent):
    # Partiers use the 'group' attribute, which exists in ABMtools.Agent, to define their group
    # They are either happy or unhappy as function of the boringness of their group and the
    # current tolerance, and are either male (M) or female (F)
    def __init__(self, controller, sex, happy=False, *args, **kwargs):
        ABMtools.Agent.__init__(self, controller, *args, **kwargs)
        self.sex = sex
        self.happy = happy

    def update_happiness(self):
        othergenderratio = len([i for i in self.controller.group(self.group).members if i.sex != self.sex]) / len([i for i in self.controller.group(self.group).members])
        self.happy = othergenderratio <= (self.controller.tolerance / 100)


########################################################################################

# One run of the model can go like this
def setup(n=300, k=15, tolerance=70):
        ### Setup
        # Create the party
    c = Party(n, k, tolerance)
        # Populate the party
    c.create_groups(c.k)
    for _ in range(n):
        c.create_agents(1, Partier, sex=random.choice(["M","F"]), group=random.choice([i.ident for i in c.groups]))

        # Collect partygoers into groups
    c.census()

        # Get everyone's initial happiness
    for a in c.agents:
        a.update_happiness()

        # Count boring groups at the start
    c.count_boring()

    return c

def step(c, i):
        ### One Step
        # Stop if all turtles are happy
    #print("Happy agents: {}".format(sum([a.happy for a in c.agents])))
    if all([a.happy for a in c.agents]):
        print("ALL AGENTS HAPPY, TERMINATING")
        print("Step {}".format(i))
        print("Boring groups: {}".format(c.boringgroups))
        for g in c.groups:
            print([str(i.sex) for i in g.members])
        sys.exit()

        # Update group memberships
    c.census()

        # Update happiness and find new groups for unhappy agents
    for a in c.agents:
        a.update_happiness()
        if not a.happy:
            a.group = random.choice(ABMtools.other(a.group, [i.ident for i in c.groups]))

        # Count the number of boring groups
    c.count_boring()

        # FOR NOW WE WILL USE THE CONSOLE TO OUTPUT AN UPDATE EACH STEP
    #print("Step {}".format(i))
    #print("Boring groups: {}".format(c.boringgroups))

c = setup()
for i in range(200):
    step(c, i)