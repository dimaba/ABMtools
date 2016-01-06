import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import abmtools
import pickle
import pytest
import random

# SETUP TEST ENVIRONMENT
def clean_start():
    print('### ###  Reloading start state  ### ###')
    cin = pickle.load(open('setup.p', 'rb'))
    abmtools.a_ident=100000
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
    print("Testing abmtools.Controller.create_agents() with base class Agent")
    print('Expected behavior: Creates N agents with given properties and adds it to agent list')
    print('Tested with N=7')
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=abmtools.Agent, agentlist='agents', group=1)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    # DERIVED CLASS TEST
    class Person(abmtools.Agent):
        a_ident = 0
        def __init__(self, controller, sex="M", happy=False, *args, **kwargs):
            abmtools.Agent.__init__(self, controller, *args, **kwargs)
            self.sex = sex
            self.happy = happy

    print("Testing abmtools.Controller.create_agents() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=Person, agentlist='agents', sex="M", group=2)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    print("Testing abmtools.Controller.cra() with base class Agent")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=abmtools.Agent, agentlist='agents', group=3)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)
    agentsatstart = len(c.agents)

    print("Testing abmtools.Controller.cra() with derived class Person")
    print("Number of agents: {}".format(len(c.agents)))
    c.create_agents(n=N, agenttype=Person, agentlist='agents', sex="M", group=4)
    print("Number of agents: {}".format(len(c.agents)))
    print("Latest agent: {}".format(c.agents[-1]))
    assert len(c.agents) == (agentsatstart + N)


def test_clear_groups():
    new_test()
    c, g, a = clean_start()
    print('Testing abmtools.Controller.clear_agents() without kill')
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
    print('Testing abmtools.Controller.clear_agents() with kill')
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
    print('Testing abmtools.Controller.kill() by passing agent')
    print('Expected behavior: Agent is removed from agent list, agent has group set to None')
    print('Agent is removed from group member list')
    print('Agent to kill: {}'.format(a))
    print('Agent to kill is in agent list before? {}'.format(a in c.agents))
    print('Agent group ident before: {}'.format(a.group.ident))
    print('Agent is in group member list before? {}'.format(a in a.group.members))
    assert (a in c.agents) and (a in a.group.members)
    aident = a.ident
    aoldgroup = a.group
    c.kill(a)
    print('Agent is in agent list after? {}'.format(aident in [i.ident for i in c.agents]))
    print('Agent is in group member list after? {}'.format(aident in [i.ident for i in aoldgroup.members]))
    assert (aident not in [i.ident for i in c.agents]) and (aident not in [i.ident for i in aoldgroup.members])


def test_agent():
    new_test()
    c, g, a = clean_start()
    print('Testing abmtools.Controller.agent() with an ident which corresponds to exactly one agent')
    print('Expected behavior: Returns agent instance with specified ident')
    print('Ident to find: {}, Agents with this ident: {}'.format(5000, len([x for x in c.agents if x.ident == 5000])))
    print('Corresponding agent: {}'.format(next(x for x in c.agents if x.ident == 5000)))
    print('Agent found: {}'.format(c.agent(5000)))
    print('Testing abmtools.Controller.agent() with an ident for which no corresponding agent exists')
    print('Expected behavior: Raises KeyError')
    c.kill(ident=5000)
    print('Ident to find: {}, Agents with this ident: {}'.format(5000, len([x for x in c.agents if x.ident == 5000])))
    with pytest.raises(KeyError) as excinfo:
        c.agent(5000)
    print('Exception raised: "{}: {}"'.format(excinfo.type, excinfo.value))
    print('Testing abmtools.Controller.agent() with an ident for which more than one corresponding agent exists')
    print('Expected behavior: Raises KeyError')
    c.create_agents(2, ident=5000)
    print('Ident to find: {}, Agents with this ident: {}'.format(5000, len([x for x in c.agents if x.ident == 5000])))
    with pytest.raises(KeyError) as excinfo:
        c.agent(5000)
    print('Exception raised: "{}: {}"'.format(excinfo.type, excinfo.value))


def test_group():
    new_test()
    c, g, a = clean_start()
    print('Testing abmtools.Controller.group() with an ident which corresponds to exactly one group')
    print('Expected behavior: Returns agent instance with specified agent')
    print('Ident to find: {}, Groups with this ident: {}'.format(500, len([x for x in c.groups if x.ident == 500])))
    print('Corresponding group: {}'.format(next(x for x in c.groups if x.ident == 500)))
    print('Group found: {}'.format(c.group(500)))
    print('Testing abmtools.Controller.group() with an ident for which no corresponding group exists')
    print('Expected behavior: Raises KeyError')
    c.groups.remove(next(x for x in c.groups if x.ident == 500))
    print('Ident to find: {}, Groups with this ident: {}'.format(500, len([x for x in c.groups if x.ident == 500])))
    with pytest.raises(KeyError) as excinfo:
        c.group(500)
    print('Exception raised: "{}: {}"'.format(excinfo.type, excinfo.value))
    print('Testing abmtools.Controller.group() with an ident for which more than one corresponding group exists')
    print('Expected behavior: Raises KeyError')
    c.create_groups(2, ident=500)
    print('Ident to find: {}, Groups with this ident: {}'.format(500, len([x for x in c.groups if x.ident == 500])))
    with pytest.raises(KeyError) as excinfo:
        c.group(500)
    print('Exception raised: "{}: {}"'.format(excinfo.type, excinfo.value))


def test_census():
    new_test()
    c = abmtools.Controller()
    print('Testing abmtools.Controller.census()')
    print('Expected behavior: all agents are in their respective groups, all groups are complete')
    abmtools.a_ident, abmtools.g_ident = 0, 0
    c.create_groups(10)
    print('Create 10 groups: {}'.format([x.ident for x in c.groups]))
    for i in range(10):
        c.create_agents(10, group=c.group(i))
    rd = {i: len([a for a in c.agents if a.group == i]) for i in range(10)}
    print('Create 100 agents, 10 per group: {}'.format(rd))
    print('Length of group member lists before census: {}'.format([len(x.members) for x in c.groups]))
    print('Reported group sizes as group property before census: {}'.format([x.size for x in c.groups]))
    c.census()
    print('Length of group member lists after census: {}'.format([len(x.members) for x in c.groups]))
    print('Reported group sizes as group property after census: {}'.format([x.size for x in c.groups]))
    print('Are all agents present in the member lists of their corresponding group? {}'.format(all([a in a.group.members for a in c.agents])))
    assert(all([x.size == 10 for x in c.groups]) and all([len(x.members) == 10 for x in c.groups]))
    assert(all([a in a.group.members for a in c.agents]))


###########################################################################
test_create_agents()
test_clear_groups()
test_kill()
test_agent()
test_group()
test_census()