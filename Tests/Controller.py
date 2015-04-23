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

def new_test():
    print('\n')
    print('### ### ### ### ### ### ### ### ### ###')

def test_create_agents(N=7):
    new_test()
    c, g, a = clean_start()
    agentsatstart = len(c.agents)
    print("Testing ABMtools.Controller.create_agents() with base class Agent")
    print('Expected behavior: Creates N agents with given properties and adds it to agent list')
    print('Tested with N=7')
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=ABMtools.Agent, agentlist='agents', group=1)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    # DERIVED CLASS TEST
    class Person(ABMtools.Agent):
        a_ident = 0
        def __init__(self, controller, sex="M", happy=False, *args, **kwargs):
            ABMtools.Agent.__init__(self, controller, *args, **kwargs)
            self.sex = sex
            self.happy = happy

    print("Testing ABMtools.Controller.create_agents() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=Person, agentlist='agents', sex="M", group=2)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    print("Testing ABMtools.Controller.cra() with base class Agent")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=ABMtools.Agent, agentlist='agents', group=3)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    print("Testing ABMtools.Controller.cra() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=Person, agentlist='agents', sex="M", group=4)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)


def test_clear_groups():
    new_test()
    c, g, a = clean_start()
    print('Testing ABMtools.Controller.clear_agents() without kill')
    print('Expected behavior: All groups are without members. All agents get group set to None')
    print('Equal number of agents in list before and after')
    print('Agents in list before: {}'.format(len(c.agents)))
    print('All groups have 0 members before? {}'.format(all([x.size == 0 for x in c.groups])))
    print('All agents have group set to None before? {}'.format(all(i.group is None for i in c.agents)))
    len_start = len(c.agents)
    c.clear_groups()
    print('Agents in list after: {}'.format(len(c.agents)))
    print('All groups have 0 members after? {}'.format(all([x.size == 0 for x in c.groups])))
    print('All agents have group set to None after? {}'.format(all(i.group is None for i in c.agents)))
    assert (len(c.agents) == len_start) and (all([x.size == 0 for x in c.groups])) and (all(i.group is None for i in c.agents))
    ct, gt, at = clean_start()
    print('Testing ABMtools.Controller.clear_agents() with kill')
    print('Expected behavior: All groups are without members. All agents get group set to None')
    print('Agent list is empty after')
    print('Agents in list before: {}'.format(len(c.agents)))
    print('All groups have 0 members before? {}'.format(all([x.size == 0 for x in ct.groups])))
    print('All agents have group set to None before? {}'.format(all(i.group is None for i in ct.agents)))
    ct.clear_groups(kill=True)
    print('Agents in list after: {}'.format(len(ct.agents)))
    print('All groups have 0 members after? {}'.format(all([x.size == 0 for x in ct.groups])))
    print('All agents have group set to None after? {}'.format(all(i.group is None for i in ct.agents)))
    assert (len(ct.agents) == 0) and (all([x.size == 0 for x in ct.groups])) and (all(i.group is None for i in ct.agents))

def test_kill():
    new_test()
    c, g, a = clean_start()
    print('Testing ABMtools.Controller.kill() by passing agent')
    print('Expected behavior: Agent is removed from agent list, agent has group set to None')
    print('Agent is removed from group member list')
    print('Agent to kill: {}'.format(a))
    print('Agent to kill is in agent list before? {}'.format(a in c.agents))
    print('Agent group before: {}'.format(a.group))
    print('Agent is in group member list before? {}'.format(a in c.group(a.group).members))
    assert (a in c.agents) and (a in c.group(a.group).members)
    aident = a.ident
    aoldgroup = a.group
    c.kill(a)
    print('Agent is in agent list after? {}'.format(aident in [i.ident for i in c.agents]))
    print('Agent is in group member list after? {}'.format(aident in [i.ident for i in c.group(aoldgroup).members]))
    assert (aident not in [i.ident for i in c.agents]) and (aident not in [i.ident for i in c.group(aoldgroup).members])
###########################################################################
test_create_agents()
test_clear_groups()
test_kill()