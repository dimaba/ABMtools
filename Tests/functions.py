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
    new_test()
    c, g, a = clean_start()
    print('Test ABMtools.other()')
    print('Expected behavior: others() returns copy of input agentset, excluding given agent')
    print("Length of g.members: {}".format(len(g.members)))
    print("First member: {}".format(g.members[0]))
    lengthatstart = len(g.members)
    others = ABMtools.other(a, g.members)
    print("Length of other members: {}".format(len(others)))
    print("First other member: {}".format(others[0]))
    print("Agent in others? {}".format(a in others))
    assert (a not in others) and (len(others) == lengthatstart - 1)

def test_compile_typeset():
    new_test()
    c, g, a = clean_start()
    print('Test ABMtools.compile_typeset with Agent')
    print('Expected behavior: input of 2 agents and 2 iterables (each n=4 agents), returns one list of all 10 agents')
    a, b = ABMtools.Agent(c), ABMtools.Agent(c)
    print('First individual: {}'.format(a))
    it1, it2 = [ABMtools.Agent(c) for _ in range(4)], [ABMtools.Agent(c) for _ in range(4)]
    returnset = ABMtools.compile_typeset([a, b], [it1, it2])
    print('Length of result: {}'.format(len(returnset)))
    print('First member: {}'.format(returnset[0]))
    assert (len(returnset) == 10)

    # It can do the same thing with groups
    print('Test ABMtools.compile_typeset with Group')
    print('Expected behavior: input of 2 groups and 2 iterables (each n=4 groups), returns one list of all 10 groups')
    a, b = ABMtools.Group(c), ABMtools.Group(c)
    print('First group: {}'.format(a))
    it1, it2 = [ABMtools.Group(c) for _ in range(4)], [ABMtools.Group(c) for _ in range(4)]
    returnset = ABMtools.compile_typeset([a, b], [it1, it2], ABMtools.Group)
    print('Length of result: {}'.format(len(returnset)))
    print('First member group: {}'.format(returnset[0]))
    assert (len(returnset) == 10)

###########################################################################
test_others()
test_compile_typeset()