import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import ABMtools
import pickle
import random
import partymodel

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


def test_define_setup():
    new_test()
    print('Test ABMtools.Ticker.set_setup() / '
          'ABMtools.Ticker.setup() with simple setup function that prints "SETUP COMPLETE"')
    print('Expected behavior: an entered function can be executed by calling Ticker.setup()')
    def example_setup():
        print("SETUP COMPLETE")
    t = ABMtools.Ticker()
    t.set_setup(example_setup)
    print("Ticker.setup_func is assigned a function object and its arguments: {}".format(t.setup_func))
    t.setup()

    print('Test ABMtools.Ticker.set_setup() / ABMtools.Ticker.setup() with realistic setup function '
          'which returns a controller object')
    print('Expected behavior: an entered function can be executed by calling Ticker.setup()')
    t = ABMtools.Ticker()
    t.set_setup(partymodel.setup, n=70, k=10, tolerance=25)
    print("Ticker.setup_func is assigned a function object and its arguments: {}".format(t.setup_func))
    c = t.setup()
    print("Returned controller object: {}, attributes: n={} k={} tolerance={} agents={} "
          "groups={}".format(c, c.n, c.k, c.tolerance, len(c.agents), len(c.groups)))

###########################################################################
test_define_setup()