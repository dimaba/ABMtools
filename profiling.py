import ABMtools
import random
import cProfile
import pstats

c = ABMtools.Controller()
for i in range(100000):
    c.create_agents(1, group=random.randint(0,1000))
for i in range(1000):
    c.create_groups(1)

g = random.choice(c.groups)
def collect_all():
    for x in c.groups:
        x.collect_members()

cProfile.run('c.census()', 'Profiles/Controller_census')
p = pstats.Stats('Profiles/Controller_census')
p.strip_dirs().sort_stats('cumulative').print_stats()