import ABMtools
import random
import pickle

c = ABMtools.Controller()
for i in range(100000):
    c.create_agents(1, group=None)
for i in range(1000):
    c.create_groups(1)
for a in c.agents:
    a.group = random.choice(c.groups)

pickle.dump(c, open('setup.p', 'wb'))