import ABMtools
import random
import cProfile
import pstats
import pickle

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

def profile_census():
    new_test()
    cProfile.run('c.census()', 'Profiles/Controller_census')
    p = pstats.Stats('Profiles/Controller_census')
    p.strip_dirs().sort_stats('cumulative').print_stats()

def test_hatch():
    print('Test ABMtools.Agent.Hatch()')
    print('Expected behavior: An agent is created which is an exact copy of original agent, except for ident')
    a = ABMtools.Agent(c, group=1)
    print('Original agent: {}'.format(a))
    b = a.hatch()
    print('New agent: {}'.format(b))


def profile_hatch():
    new_test()
    cProfile.run('test_hatch()', 'Profiles/Agent_hatch')
    p = pstats.Stats('Profiles/Agent_hatch')
    p.strip_dirs().sort_stats('cumulative').print_stats()


def test_kill():
    a = random.choice(c.agents)
    c.kill(agent=a)


def profile_kill():
    new_test()
    cProfile.run('test_kill()', 'Profiles/Controller_kill')
    p = pstats.Stats('Profiles/Controller_kill')
    p.strip_dirs().sort_stats('cumulative').print_stats()


def test_clear_groups(kill=True):
    print('Testing ABMtools.Controller.clear_agents() with kill')
    print('Expected behavior: All groups are without members. All agents get group set to None')
    print('Agent list is empty after')
    print('Agents in list before: {}'.format(len(c.agents)))
    print('All groups have 0 members before? {}'.format(all([x.size == 0 for x in c.groups])))
    print('All agents have group set to None before? {}'.format(all(i.group is None for i in c.agents)))
    ab = c.agents
    c.clear_groups(kill=kill)
    print('Agents in list after: {}'.format(len(c.agents)))
    print('All groups have 0 members after? {}'.format(all([x.size == 0 for x in c.groups])))
    print('All agents have group set to None after? {}'.format(all(i.group is None for i in ab)))


def profile_clear_group():
    new_test()
    cProfile.run('test_clear_groups()', 'Profiles/Controller_clear_groups')
    p = pstats.Stats('Profiles/Controller_clear_groups')
    p.strip_dirs().sort_stats('cumulative').print_stats()


###########################################################################
c, g, a = clean_start()
profile_clear_group()