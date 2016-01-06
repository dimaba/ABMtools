import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import pickle
import ABMtools

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

def test_tie_creation():
    new_test()
    print('Test ABMtools.Tie() creation')
    print('Expected behavior: Raises NotImplementedError as ties are not yet implemented')
    try:
        t = ABMtools.Tie()
        assert False
    except NotImplementedError as e:
        print(e)


###########################################################################
c, g, a = clean_start()
test_tie_creation()