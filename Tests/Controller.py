import ABMtools
import pickle
import random

# SETUP TEST ENVIRONMENT
c = pickle.load(open('setup.p', 'rb'))
ABMtools.a_ident=100000
c.census()
g = c.groups[0]
a = g.members[0]

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_create_agents():
    new_test()
    print("Testing ABMtools.Controller.create_agents() with base class Agent")
    print('Expected behavior: Creates N agents with given properties and adds it to agent list')
    print('Tested with N=7')
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=7, agenttype=ABMtools.Agent, agentlist='agents', group=1)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))

    # DERIVED CLASS TEST
    class Person(ABMtools.Agent):
        a_ident = 0
        def __init__(self, controller, sex="M", happy=False, *args, **kwargs):
            ABMtools.Agent.__init__(self, controller, *args, **kwargs)
            self.sex = sex
            self.happy = happy

    print("Testing ABMtools.Controller.create_agents() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=7, agenttype=Person, agentlist='agents', sex="M", group=2)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))

    print("Testing ABMtools.Controller.cra() with base class Agent")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=7, agenttype=ABMtools.Agent, agentlist='agents', group=3)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))

    print("Testing ABMtools.Controller.cra() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=7, agenttype=Person, agentlist='agents', sex="M", group=4)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))

###########################################################################
test_create_agents()