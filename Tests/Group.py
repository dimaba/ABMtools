import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
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

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_group_creation():
    new_test()
    c = ABMtools.Controller()
    print('Test ABMtools.Group() creation')
    print('Expected behavior: Two groups are created')
    a,b = ABMtools.Group(c), ABMtools.Group(c)
    print('Group 1: {}, Group 2: {}'.format(a, b))


def test_collect_members():
    new_test()
    c, g, a = clean_start()
    print('Test ABMtools.Group.collect_members() on fresh data')
    print('Expected behavior: Should collect all agents in an agentset whose group number matches ident of group')
    a_set = [ABMtools.Agent(c) for _ in range(10)]
    for na in a_set:
        na.group = random.choice([1,2])
    ng = ABMtools.Group(c, ident=1)
    ng.collect_members(a_set)
    print('Agents with correct group number: {}'.format(len([na for na in a_set if na.group == 1])))
    print('Collected agents: {}'.format(len(ng.members)))
    assert len([na for na in a_set if na.group == 1]) == len(ng.members)

    print('Test ABMtools.Group.collect_members() on known data')
    print('Expected behavior: Number of members in group should be the same before and after collecting')
    print('(In known data groups already have correct member lists.)')
    print('Number of members before: {}'.format(len(g.members)))
    lengthatstart = len(g.members)
    g.collect_members()
    print('Number of members after: {}'.format(len(g.members)))
    assert (len(g.members) == lengthatstart)


def test_ungroup():
    new_test()
    c, g, a = clean_start()
    print('Test ABMtools.Group.ungroup() without killing agents')
    print('Expected behavior: All members are removed from the group.')
    print('Member list is left empty and agents are given None group')
    print('Agents are still in controller agent list')
    print('Number of members before: {}'.format(len(g.members)))
    print('Number of agents before: {}'.format(len(c.agents)))
    membersatstart = len(g.members)
    agentsatstart = len(c.agents)
    # Save members
    gsave = g.members
    # Ungroup without killing
    g.ungroup()
    print('Number of members after in g.members: {}'.format(len(g.members)))
    print('Number of members after from agentlist: {}'.format(len([i for i in c.agents if i.group == g.ident])))
    print('Number of agents after: {}'.format(len(c.agents)))
    assert (len(g.members) == 0) and (len([i for i in c.agents if i.group == g.ident]) == 0) and (len(c.agents) == agentsatstart)

    # Restore members
    c, g, a = clean_start()
    print('Test ABMtools.Group.ungroup() with killing agents')
    print('Expected behavior: All members are removed from the group.')
    print('Member list is left empty and agents are given None group')
    print('Agents are removed from controller agent list')
    print('Number of members before: {}'.format(len(g.members)))
    print('Number of agents before: {}'.format(len(c.agents)))
    # Ungroup with killing
    g.ungroup(kill=True)
    print('Number of members after in g.members: {}'.format(len(g.members)))
    print('Number of members after from agentlist: {}'.format(len([i for i in c.agents if i.group == g.ident])))
    print('Number of agents after: {}'.format(len(c.agents)))
    assert (len(g.members) == 0) and (len(c.agents) == agentsatstart - membersatstart)


def test_sprout():
    new_test()
    c, g, a = clean_start()
    print('Test ABMtools.Group.sprout()')
    print('Expected behavior: sprout() returns N agents with set group')
    print('Agents should be appended to group.members and to controller.agents')
    print('Tested with N=2')
    print("Length of g.members before: {}".format(len(g.members)))
    print("Length of c.agents before: {}".format(len(c.agents)))
    print("Last group member before: {}".format(g.members[-1]))
    membersbefore = len(g.members)
    agentsbefore = len(c.agents)
    # Sprout two new members with default arguments
    g.sprout(2)
    print("Length of g.members after: {}".format(len(g.members)))
    print("Length of c.agents after: {}".format(len(c.agents)))
    print("Last group member after: {}".format(g.members[-1]))
    assert (len(g.members) == membersbefore + 2) and (len(c.agents) == agentsbefore + 2)

###########################################################################
test_group_creation()
test_collect_members()
test_ungroup()
test_sprout()
