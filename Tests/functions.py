import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import ABMtools
import pickle

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

# Test ABMtools.other()
def test_others():
    # Expected behavior: others() returns copy of input agentset, excluding given agent
    new_test()
    print('Test ABMtools.other()')
    print("Length of g.members: {}".format(len(g.members)))
    print("First member: {}".format(g.members[0]))
    others = ABMtools.other(a, g.members)
    print("Length of other members: {}".format(len(others)))
    print("First other member: {}".format(others[0]))
    try:
        print(others.index(a))
    except ValueError:
        print("Agent is not in Others")

def test_compile_typeset():
    # Expected behavior: given input of 2 agents and 2 iterables (each of n=4 agents) returns one list
    # of all 10 agents
    new_test()
    print('Test ABMtools.compile_typeset with Agent')
    a,b = ABMtools.Agent(c), ABMtools.Agent(c)
    print('First individual: {}'.format(a))
    it1, it2 = [ABMtools.Agent(c) for _ in range(4)],[ABMtools.Agent(c) for _ in range(4)]
    returnset = ABMtools.compile_typeset([a,b],[it1,it2])
    print('Length of result: {}'.format(len(returnset)))
    print('First member: {}'.format(returnset[0]))

    # It can do the same thing with groups
    print('Test ABMtools.compile_typeset with Group')
    a,b = ABMtools.Group(c), ABMtools.Group(c)
    print('First group: {}'.format(a))
    it1, it2 = [ABMtools.Group(c) for _ in range(4)],[ABMtools.Group(c) for _ in range(4)]
    returnset = ABMtools.compile_typeset([a,b],[it1,it2],ABMtools.Group)
    print('Length of result: {}'.format(len(returnset)))
    print('First member group: {}'.format(returnset[0]))

###########################################################################
c, g, a = clean_start()
test_others()
test_compile_typeset()