import ABMtools
import pickle
import random

# SETUP TEST ENVIRONMENT
c = pickle.load(open('setup.p', 'rb'))
ABMtools.Agent.a_ident=100000
c.census()
g = c.groups[0]
a = g.members[0]

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_create():
    # Expected behavior: one group is created
    new_test()
    ng1,ng2 = ABMtools.Group(c), ABMtools.Group(c)
    print(ng1, ng2)

def test_sprout():
    # Expected behavior: sprout() returns n agents with set group
    # Agents should be appended to group.members and to controller.agents
    new_test()
    print('Testing ABMtools.Group.sprout()')
    print("Length of g.members: {}".format(len(g.members)))
    print("Length of c.agents: {}".format(len(c.agents)))
    print("Last group member: {}".format(g.members[-1]))
    # Sprout two new members with default arguments
    g.sprout(2)
    print("Length of g.members: {}".format(len(g.members)))
    print("Length of c.agents: {}".format(len(c.agents)))
    print("Last group member: {}".format(g.members[-1]))


###########################################################################
test_create()
test_sprout()