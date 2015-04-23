import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import ABMtools
import pickle
import random

# SETUP TEST ENVIRONMENT
def clean_start():
    print('### ###  Reloading start state  ### ###')
    cin = pickle.load(open('setup.p', 'rb'))
    ABMtools.a_ident=100000
    cin.census()
    gin = cin.groups[0]
    ain = gin.members[0]
    return cin, gin, ain

# DERIVED CLASS TEST
class Person(ABMtools.Agent):
    def __init__(self, controller, sex="M", happy=False, *args, **kwargs):
        ABMtools.Agent.__init__(self, controller, *args, **kwargs)
        self.sex = sex
        self.happy = happy

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_agent_creation():
    new_test()
    print('Test ABMtools.Agent() creation')
    print('Expected behavior: Two agents are created')
    a,b = ABMtools.Agent(c), ABMtools.Agent(c)
    print('Agent 1: {}, Agent 2: {}'.format(a,b))

def test_hatch():
    new_test()
    print('Test ABMtools.Agent.Hatch()')
    print('Expected behavior: An agent is created which is an exact copy of original agent, except for ident.')
    print('This new agent must not be a reference to the same instance as old agent.')
    a = ABMtools.Agent(c, group=1)
    print('Original agent before: {}'.format(a))
    b = a.hatch()
    print('Original agent after: {}'.format(a))
    print('New agent: {}'.format(b))
    print('Both are not the same object: {}'.format(a is not b))

###########################################################################
c, g, a = clean_start()
test_agent_creation()
test_hatch()