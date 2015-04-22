import ABMtools

c = ABMtools.Controller()
# Test agent creation
a,b = ABMtools.Agent(c), ABMtools.Agent(c)
print(a,b)

# Test Hatch Function
print('Test Hatch()')
a = ABMtools.Agent(c, group=1)
print(a)
b = a.hatch()
print(b)

