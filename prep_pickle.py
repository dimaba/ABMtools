import ABMtools
import random
import pickle

c = ABMtools.Controller()
for i in range(100000):
    c.create_agents(1, group=random.randint(0,999))
for i in range(1000):
    c.create_groups(1)

pickle.dump(c, open('setup.p', 'wb'))