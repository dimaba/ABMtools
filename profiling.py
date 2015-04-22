import ABMtools
import random
import cProfile
import pstats
import pickle

c = pickle.load(open('setup.p', 'rb'))
print(c)

cProfile.run('c.census()', 'Profiles/Controller_census')
p = pstats.Stats('Profiles/Controller_census')
p.strip_dirs().sort_stats('cumulative').print_stats()