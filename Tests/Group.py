import ABMtools
import pickle
import random

# SETUP TEST ENVIRONMENT
c = pickle.load(open('setup.p', 'rb'))
ABMtools.a_ident=100000
c.census()
g = c.groups[0]
na = g.members[0]

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_group_creation():
    new_test()
    print('Test ABMtools.Group() creation')
    print('Expected behavior: Two groups are created')
    a,b = ABMtools.Group(c), ABMtools.Group(c)
    print('Group 1: {}, Group 2: {}'.format(a,b))


def test_collect_members():
    new_test()
    print('Test ABMtools.Group.collect_members() on fresh data')
    print('Expected behavior: Should collect all agents in an agentset whose group number matches ident of group')
    a_set = [ABMtools.Agent(c) for _ in range(10)]
    for na in a_set:
        na.group = random.choice([1,2])
    ng = ABMtools.Group(c, ident=1)
    ng.collect_members(a_set)
    print('Agents with correct group number: {}'.format(len([na for na in a_set if na.group == 1])))
    print('Collected agents: {}'.format(len(ng.members)))

    print('Test ABMtools.Group.collect_members() on known data')
    print('Expected behavior: Number of members in group should be the same before and after collecting')
    print('(In known data groups already have correct member lists.)')
    print('Number of members before: {}'.format(len(g.members)))
    g.collect_members()
    print('Number of members after: {}'.format(len(g.members)))


def test_ungroup():
    new_test()
    print('Test ABMtools.Group.ungroup() without killing agents')
    print('Expected behavior: All members are removed from the group.')
    print('Member list is left empty and agents are given None group')
    print('Agents are still in controller agent list')
    print('Number of members before: {}'.format(len(g.members)))
    print('Number of agents before: {}'.format(len(c.agents)))
    # Save members
    gsave = g.members
    # Ungroup without killing
    g.ungroup()
    print('Number of members after in g.members: {}'.format(len(g.members)))
    print('Number of members after from agentlist: {}'.format(len([i for i in c.agents if i.group == g.ident])))
    print('Number of agents after: {}'.format(len(c.agents)))
    # Restore members
    g.members = gsave
    for i in gsave:
        i.group = g.ident
    g.update_size()

    print('Test ABMtools.Group.ungroup() with killing agents')
    print('Expected behavior: All members are removed from the group.')
    print('Member list is left empty and agents are given None group')
    print('Agents are removed from controller agent list')
    print('Number of members before: {}'.format(len(g.members)))
    print('Number of agents before: {}'.format(len(c.agents)))
    # Save members
    gsave = list(g.members)
    # Ungroup without killing
    g.ungroup(kill=True)
    print('Number of members after in g.members: {}'.format(len(g.members)))
    print('Number of members after from agentlist: {}'.format(len([i for i in c.agents if i.group == g.ident])))
    print('Number of agents after: {}'.format(len(c.agents)))
    # Restore members
    c.agents += gsave
    for i in gsave:
        i.group = g.ident
    g.collect_members()


def test_sprout():
    new_test()
    print('Test ABMtools.Group.sprout()')
    print('Expected behavior: sprout() returns n agents with set group')
    print('Agents should be appended to group.members and to controller.agents')
    print("Length of g.members before: {}".format(len(g.members)))
    print("Length of c.agents before: {}".format(len(c.agents)))
    print("Last group member before: {}".format(g.members[-1]))
    # Sprout two new members with default arguments
    g.sprout(2)
    print("Length of g.members after: {}".format(len(g.members)))
    print("Length of c.agents after: {}".format(len(c.agents)))
    print("Last group member after: {}".format(g.members[-1]))


###########################################################################
test_group_creation()
test_collect_members()
test_ungroup()
test_sprout()
