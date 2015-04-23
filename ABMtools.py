import copy
a_ident = 0
g_ident = 0

class Agent:
    @staticmethod
    def get_ident():
        global a_ident
        ident = a_ident
        a_ident += 1
        return ident

    def __init__(self, controller, group=None, ident=None):
        # Group = ident nr of group
        self.controller = controller
        if ident is not None:
            self.ident = ident
        else:
            self.ident = self.get_ident()
        self.group = group

    def __str__(self):
        return "Type = Agent, Identity = {}, Group = {}".format(self.ident, self.group)

    def hatch(self):
        # Create one new turtle in the same group which copies all attributes other than ident
        new_agent = copy.copy(self)
        new_agent.ident = new_agent.get_ident()
        return new_agent
        
        
class Group:

    @staticmethod
    def get_ident():
        global g_ident
        ident = g_ident
        g_ident += 1
        return ident

    def __init__(self, controller, size=None, members=None, ident=None):
        if members is None:
            members = []
        self.controller = controller
        if ident is not None:
            self.ident = ident
        else:
            self.ident = self.get_ident()
        self.size = size
        self.members = members
        
    def __str__(self):
        return "Type = Group, Identity = {}, size = {}".format(self.ident, self.size)

    def str_members(self):
        return [str(m) for m in self.members]

    def update_size(self):
        self.size = len(self.members)

    def increment_size(self):
        self.size += 1

    def decrement_size(self):
        self.size -= 1

    def collect_members(self, agents=None):
        if agents is None:
            agents = self.controller.agents
        self.members = []
        for a in agents:
            if a.group == self.ident:
                self.members.append(a)
        self.update_size()

    def ungroup(self, kill=False, controller=None):
        # Remove all members from the group
        # Sets member group values to None if kill is False
        # Destroys group members if kill is True
        if controller is None:
            controller = self.controller
        if not kill:
            for agent in self.members:
                agent.group = None
            self.members = []
        else:
            while len(self.members) > 0:
                self.members[0].group = None
                controller.kill(agent=self.members[0])
                self.members.pop(0)
            self.members = []
        self.update_size()

    def sprout(self, n, *args, **kwargs):
        # Create n new agents in this group
        agents = []
        for _ in range(n):
            agents.append(Agent(controller=self.controller, group=self.ident, *args, **kwargs))

        self.members += agents
        self.controller.agents += agents

        
class Tie:
    pass

    
class Controller:
    def __init__(self, agents=None, groups=None):
        if agents is None:
            self.agents = []
        else:
            self.agents = agents
        if groups is None:
            self.groups = []
        else:
            self.groups = groups

    def create_agents(self, n=1, agenttype=Agent, agentlist='agents', *args, **kwargs):
        # Create agents of specified type (defaults to ABMtools.Agent) with the
        # possibility to pass them setup arguments
        setattr(self, agentlist, getattr(self, agentlist) + [agenttype(self, *args, **kwargs) for _ in range(n)])
        
    def cra(self, *args, **kwargs):
        # Shorthand for Controller.create_agents() for lazy people who hate
        # clarity
        self.create_agents(*args, **kwargs)
        
    def clear_agents(self):
        # Removes all agents
        self.agents = []
        
    def ca(self):
        # Shorthand for Controller.clear_agents()
        self.clear_agents()
        
    def create_groups(self, n=1, grouptype=Group, grouplist='groups', *args, **kwargs):
        # Create groups of specified type (defaults to ABMtools.Group) with the
        # possibility to pass them setup arguments
        setattr(self, grouplist, getattr(self, grouplist) + [grouptype(self, *args, **kwargs) for _ in range(n)])

    def crg(self, *args, **kwargs):
        self.create_groups(*args, **kwargs)

    def clear_groups(self, kill=False):
        # Destroy all groups. Kill determines whether all members of these
        # groups are killed or not
        for agent in self.agents:
            agent.group = None
        for group in self.groups:
            group.members = []
            group.update_size()
        self.groups = []
        if kill:
            self.agents = []
        
    def cg(self, *args, **kwargs):
        self.clear_groups(*args, **kwargs)

    def clear_ties(self):
        pass

    def cl(self):
        self.clear_ties()

    def clear_all(self):
        self.clear_groups()
        #self.clear_ties()
        self.clear_agents()

    def kill(self, agent=None,  ident=None):
        # Kill one specific agent
        if agent is None and ident is not None:
            agent = self.agent(ident)
                
        elif agent is None and ident is None:
            raise TypeError("Too few arguments. At least one of agent= and ident= must be specified.")
        self.agents.remove(agent)

    def agent(self, ident):
        # Returns the instance of a single agent with a given ident
        if len([x for x in self.agents if x.ident == ident]) == 1:
            agent = next(x for x in self.agents if x.ident == ident)
        elif len([x for x in self.agents if x.ident == ident]) > 1:
            raise Exception("More than one agent with ident {} found.".format(ident))
        else:
            raise Exception("No agents with ident {} found.".format(ident))
        
        return agent

    def group(self, ident):
        # Returns the instance of a single group with a given ident
        if len([x for x in self.groups if x.ident == ident]) == 1:
            group = next(x for x in self.groups if x.ident == ident)
        elif len([x for x in self.groups if x.ident == ident]) > 1:
            group = None
            Exception("More than one group with ident {} found.".format(ident))
        else:
            group = None
        
        return group

    def census(self, agents=None, groups=None):
        # Collect members for all groups
        if agents is None:
            agents = self.agents
        if groups is None:
            groups = self.groups

        for g in groups:
            g.members = []

        g_dict = dict((g.ident, g) for g in groups)
        for a in agents:
            if a.group is not None:
                g = g_dict[a.group]
                if g is not None:
                    g.members.append(a)


class Ticker:
    def __init__(self, interval=1, run=1, header="run,tick", writeheader=True):
        self.run = run
        self.ticks = 0
        self.outfile = "result_run" + str(run) + ".txt"
        self.header = header
        if writeheader:
            with open(self.outfile, "w") as f:
                f.write(header + "\n")
        self.interval = interval
        self.line = ""
        self.setline("")
        
    def tick(self):
        self.ticks += 1
        if self.ticks % self.interval == 0:
            self.write()
            
    def write(self):
        #print("F1", self.outfile)
        with open(self.outfile, "a") as f:
            f.write(self.line)
    
    def setline(self, additions):
        self.line = "{},{},".format(self.run, self.ticks) + additions + "\n"
        
    def setheader(self, additions):
        self.header = "run,tick," + additions + "\n"

    def newrun(self):
        self.run += 1
        self.ticks = 0


##############################
    
def max_one_of(agentset, var):
    # Returns agent with highest value of var in agentset
    # Returns only the first such agent even if multiple agents share
    # this maximum value
    # Input var as string
    maxval = max([getattr(agent, var) for agent in agentset])
    
    return next(agent for agent in agentset if getattr(agent, var) == maxval)


def max_n_of(agentset, var, n):
    # Return list of n agents with highest values of var in agentset
    # Returns only the first n agents if there are more with this max value
    # Returns agents with second-highest value and so on if less than n agents
    # share max value
    # Input var as string
    if n > len(agentset):
        raise ValueError('Requested n is larger than length of agentset')
    maxval = max([getattr(agent, var) for agent in agentset])
    agentswithmax = [agent for agent in agentset if getattr(agent, var) == maxval]
    if len(agentswithmax) >= n:
        return agentswithmax[:n]
    else:
        filler = max_n_of([agent for agent in agentset if getattr(agent, var) < maxval], var, (n - len(agentswithmax)))
        
    return agentswithmax + filler
    
        
def with_max(agentset, var):
    # Returns a list of all agents with the maximum value of var in agentset
    maxval = max([getattr(agent, var) for agent in agentset])
    
    return [agent for agent in agentset if getattr(agent, var) == maxval]
    
    
def min_one_of(agentset, var):
    # Returns agent with lowest value of var in agentset
    # Returns only the first such agent even if multiple agents share
    # this minimum value
    # Input var as string
    minval = min([getattr(agent, var) for agent in agentset])
    
    return next(agent for agent in agentset if getattr(agent, var) == minval)


def min_n_of(agentset, var, n):
    # Return list of n agents with lowest values of var in agentset
    # Returns only the first n agents if there are more with this max value
    # Returns agents with second-highest value and so on if less than n agents
    # share max value
    # Input var as string
    if n > len(agentset):
        raise ValueError('Requested n is larger than length of agentset')
    minval = min([getattr(agent, var) for agent in agentset])
    agentswithmin = [agent for agent in agentset if getattr(agent, var) == minval]
    if len(agentswithmin) >= n:
        return agentswithmin[:n]
    else:
        filler = min_n_of([agent for agent in agentset if getattr(agent, var) > minval], var, (n - len(agentswithmin)))
        
    return agentswithmin + filler


def with_min(agentset, var):
    # Returns a list of all agents with the minimum value of var in agentset
    minval = min([getattr(agent, var) for agent in agentset])
    
    return [agent for agent in agentset if getattr(agent, var) == minval]


def other(instance, instanceset):
    # Returns same instanceset but minus given agent
    instanceset.remove(instance)
    return instanceset

def compile_typeset(individuals=None, iterables=None, instancetype=Agent):
    # Take instances or groups of instances of a given type and compile them into one list
    typeset = []
    if individuals is not None:
        for i in individuals:
            if isinstance(i, instancetype):
                typeset.append(i)
    if iterables is not None:
        for s in iterables:
            for i in s:
                if isinstance(i, instancetype):
                    typeset.append(i)

    return typeset