import ABMtools
import random
import cProfile
import pstats
import pickle

c = pickle.load(open('setup.p', 'rb'))
print(c)


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
    cProfile.run('test_kill()', 'Profiles/Controller_kill')
    p = pstats.Stats('Profiles/Controller_kill')
    p.strip_dirs().sort_stats('cumulative').print_stats()


###########################################################################

profile_kill()