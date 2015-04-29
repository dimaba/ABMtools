import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from collections import OrderedDict
import pickle
import ABMtools
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


def partymodel_start():
    print('### ###    Loading partymodel   ### ###')
    tin = ABMtools.Ticker()
    tin.set_setup(partymodel.setup, n=70, k=10, tolerance=25)
    cin = tin.setup()
    cin.setupvars = OrderedDict([("n", "Nr.Initial.Agents"), ("k", "Nr.Initial.Groups"), ("tolerance", "Tolerance level")])
    cin.reporters = OrderedDict([("len(self.agents)", "Nr.Agents"), ("self.boringgroups", "Nr.BoringGroups")])
    return tin, cin

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
    t, c = partymodel_start()
    print("Ticker.setup_func is assigned a function object and its arguments: {}".format(t.setup_func))
    print("Returned controller object: {}, attributes: n={} k={} tolerance={} agents={} "
          "groups={}".format(c, c.n, c.k, c.tolerance, len(c.agents), len(c.groups)))


def test_header():
    new_test()
    t, c = partymodel_start()
    print("Test ABMtools.Ticker.header()")
    print("Expected behavior: writes header consisting of names of all reporters")
    c.setupvars = OrderedDict([("n", "Nr.Initial.Agents"), ("k", "Nr.Initial.Groups"), ("tolerance", "Tolerance level")])
    c.reporters = OrderedDict([("len(self.agents)", "Nr.Agents"), ("self.boringgroups", "Nr.BoringGroups")])
    print("Selected setup variables: {}".format(c.setupvars))
    print("Selected reporters: {}".format(c.reporters))
    print("Resulting header: ")
    print(t.header())

def test_report():
    new_test()
    t, c = partymodel_start()
    print("Test ABMtools.Ticker.report()")
    print("Expected behavior: writes values of all reporters")
    c.reporters = OrderedDict([("n_agents", "Nr.Agents"), ("boringgroups", "Nr.BoringGroups")])
    print("Selected reporters: {}".format(c.reporters))
    print("Values of reporters for first 3 steps: ")
    t.set_step(partymodel.step, c, t.ticks)
    rep0 = t.report()
    t.step()
    rep1 = t.report()
    t.step()
    rep2 = t.report()
    t.step()
    rep3 = t.report()
    print("0: {}1: {}2: {}3: {}".format(rep0, rep1, rep2, rep3))


###########################################################################
test_define_setup()
test_header()
test_report()