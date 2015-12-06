import collections
import copy
a_ident = 0
g_ident = 0

class Agent:
    """Create an agent.

    This class is meant to be extended with methods specific to the ABM.
    Example: if agents in the ABM should evaluate their happiness given certain conditions,
    you would want to extend this class with a 'happiness' attribute and a method to update it.

    Attributes:
    controller (ABMtools.Controller): Controller to manage this Agent
    ident (int): Agent's unique identification number
    group (int): Number of the group this Agent belongs to

    """
    @staticmethod
    def get_ident():
        """ Get current global agent ident from ABMtools module and return it."""
        global a_ident
        ident = a_ident
        a_ident += 1
        return ident

    def __init__(self, controller, group=None, ident=None):
        # Group = group object
        self.controller = controller
        if ident is not None:
            self.ident = ident
        else:
            self.ident = self.get_ident()
        self.group = group

    def __str__(self):
        return "Type = Agent, Identity = {}, Group = {}".format(self.ident, self.group)

    def hatch(self, register_with_group=True, register_with_controller=True):
        """
        Create one new agent in the same group which copies all attributes other than ident.
        By default register this new agent with original agent's group and controller
        :param register_with_group: Boolean, if True register new agent with original agent's group
        :param register_with_controller: Boolean, if True register new agent with original agent's controller
        :return: Return the new agent (in case you immediately want to make some modifications to new agent
        """
        new_agent = copy.copy(self)
        new_agent.ident = new_agent.get_ident()
        if register_with_group and self.group is not None:
            group = self.group
            group.members.append(new_agent)
            group.update_size()
        if register_with_controller and self.controller is not None:
            self.controller.agents.append(new_agent)
            self.controller.update_counts()
        return new_agent
        
        
class Group:
    """Create a group.

    This class is meant to be extended with methods specific to the ABM.
    Example: if a group in the ABM should levy a tax on its members you would want to
    extend this class with a 'tax_level' attribute and a method to collect taxes.

    Attributes:
    controller (ABMtools.Controller): Controller to manage this Group
    ident (int): Group's unique identification number
    size (int): Number of members in the Group
    members (list of ABMtools.Agent or subclasses): All agents which are a member of this group
    """
    @staticmethod
    def get_ident():
        """ Get current global group ident from ABMtools module and return it."""
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
        """Return string representation of all members of this Group."""
        return [str(m) for m in self.members]

    def update_size(self):
        """Update Group.size with the number of current members."""
        self.size = len(self.members)

    def increment_size(self):
        """Add one to Group.size."""
        self.size += 1

    def decrement_size(self):
        """Remove one from Group.size."""
        self.size -= 1

    def collect_members(self, agents=None):
        """Add all members to Group.members list.

        Args:
        agents=None (list of ABMtools.Agent or subclasses): List of agents from which to collect members

        Loop through provided list of agents (or through Group's controller's list of agents if no list provided) and
        add all agents whose Agent.group matches this Group's ident to this Group's member list. Then update size of
        the member list.
        """
        if agents is None:
            agents = self.controller.agents
        self.members = []
        for a in agents:
            if a.group == self:
                self.members.append(a)
        self.update_size()

    def ungroup(self, kill=False, controller=None):
        """Remove all members from the group.

        Args:
        kill=False (Bool): Should agents in the group also be killed? True -> Yes, False -> No
        controller=None (AB
        """
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
                a = self.members[0]
                controller.kill(a)
                a.group = None
            self.members = []
        self.update_size()

    def sprout(self, n, *args, **kwargs):
        # Create n new agents in this group
        agents = []
        for _ in range(n):
            agents.append(Agent(controller=self.controller, group=self.ident, *args, **kwargs))

        self.members += agents
        self.controller.agents += agents
        self.update_size()

        
class Tie:
    pass


class Controller:
    def __init__(self, agents=None, groups=None, reporters=None, setupvars=None):
        if agents is None:
            self.agents = []
        else:
            self.agents = agents
        if groups is None:
            self.groups = []
        else:
            self.groups = groups
        if reporters is None:
            self.reporters = collections.OrderedDict()
        else:
            self.reporters = reporters
        if setupvars is None:
            self.setupvars = collections.OrderedDict()
        else:
            self.setupvars = setupvars
        self.n_agents = len(self.agents)
        self.n_groups = len(self.groups)

    def update_counts(self):
        self.n_agents = len(self.agents)
        self.n_groups = len(self.groups)

    def create_agents(self, n=1, agenttype=Agent, agentlist='agents', *args, **kwargs):
        # Create agents of specified type (defaults to ABMtools.Agent) with the
        # possibility to pass them setup arguments
        setattr(self, agentlist, getattr(self, agentlist) + [agenttype(self, *args, **kwargs) for _ in range(n)])
        self.update_counts()
        
    def cra(self, *args, **kwargs):
        # Shorthand for Controller.create_agents() for lazy people who hate
        # clarity
        self.create_agents(*args, **kwargs)
        
    def clear_agents(self):
        # Removes all agents
        self.agents = []
        self.update_counts()
        
    def ca(self):
        # Shorthand for Controller.clear_agents()
        self.clear_agents()
        
    def create_groups(self, n=1, grouptype=Group, grouplist='groups', *args, **kwargs):
        # Create groups of specified type (defaults to ABMtools.Group) with the
        # possibility to pass them setup arguments
        setattr(self, grouplist, getattr(self, grouplist) + [grouptype(self, *args, **kwargs) for _ in range(n)])
        self.update_counts()

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
        self.update_counts()
        
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

        if agent.group is not None:
            agent.group.members.remove(agent)
            agent.group = None
        self.agents.remove(agent)
        self.update_counts()

    def move(self, agent, target_group=None, target_group_ident=None):
        """
        Move an agent from its current group to another. Both the group object and the group ident can be used
        to identify the target group. If both are given the group object is used. If neither are given the agent
        is moved to group None (i.e. out of the existing group but not to a new one)
        Updates size of original and
        target group.
        :param agent: agent to be moved
        :param target_group: group object to move agent to
        :param target_group_ident: ident of group to move agent to
        :return:
        """
        # Get target group from ident if only ident is given
        if target_group is None and target_group_ident is not None:
            target_group = self.group(target_group_ident)

        # Remove from original group if agent was in one
        original_group = agent.group
        if original_group is not None:
            original_group.members.remove(agent)
            original_group.decrement_size()

        # Move to new group if specified, else move out of all groups
        if target_group is not None:
            agent.group = target_group
            target_group.members.append(agent)
            target_group.increment_size()
        else:
            agent.group = None


    def agent(self, ident):
        # Returns the instance of a single agent with a given ident
        if len([x for x in self.agents if x.ident == ident]) == 1:
            agent = next(x for x in self.agents if x.ident == ident)
        elif len([x for x in self.agents if x.ident == ident]) > 1:
            raise KeyError("More than one agent with ident {} found.".format(ident))
        else:
            raise KeyError("No agents with ident {} found.".format(ident))
        
        return agent

    def group(self, ident):
        # Returns the instance of a single group with a given ident
        if len([x for x in self.groups if x.ident == ident]) == 1:
            group = next(x for x in self.groups if x.ident == ident)
        elif len([x for x in self.groups if x.ident == ident]) > 1:
            group = None
            raise KeyError("More than one group with ident {} found.".format(ident))
        else:
            group = None
            raise KeyError("No groups with ident {} found.".format(ident))
        
        return group

    def census(self, agents=None, groups=None):
        # Collect members for all groups
        if agents is None:
            agents = self.agents
        if groups is None:
            groups = self.groups

        for g in groups:
            g.members = []

        for a in agents:
            if a.group is not None:
                g.members.append(a)
                    
        for g in groups:
            g.update_size()


class Ticker:
    # The ticker stores summary variables across periods, handles any functions that need to be called in each step of
    # the model
    # SETUP FUNCTION MUST RETURN A CONTROLLER OBJECT
    def __init__(self, controller=None, interval=1, run=1, outfile="Results/run.txt"):
        self.run = run
        self.ticks = 0
        self.interval = interval
        self.setup_func = None
        self.step_func = None
        self.controller = controller
        self.outfile = outfile

    def set_setup(self, func, *args, **kwargs):
        self.setup_func = (func, args, kwargs)

    def setup(self, set_controller=True):
        func = self.setup_func[0]
        args = self.setup_func[1]
        kwargs = self.setup_func[2]
        c = func(*args, **kwargs)
        if set_controller:
            self.controller = c
        return c

    def header(self):
        # PLACEHOLDER
        header = ""
        setupattr = [getattr(self.controller, var) for var in self.controller.setupvars.keys()]
        for varname, value in zip(self.controller.setupvars.values(), setupattr):
            header += ("{} = {}\n".format(varname, value))
        header += ",".join([str(k) for k in self.controller.reporters.keys()]) + "\n"
        return header

    def set_step(self, func, *args, **kwargs):
        self.step_func = (func, args, kwargs)

    def step(self, write=True):
        func = self.step_func[0]
        args = self.step_func[1]
        kwargs = self.step_func[2]
        func(*args, **kwargs)
        if write and self.ticks == 0:
            self.write_to_file(self.header(), method='w')
        if write and self.ticks % self.interval in (0, 1):
            self.write_to_file(self.report(), method='a')
        self.ticks += 1
        # IF CURRENT TICK NUMBER MATCHES THE INTERVAL THIS FUNCTION SHOULD TRIGGER WRITING TO FILE

    def report(self):
        reporter_values = [str(getattr(self.controller, var)) for var in self.controller.reporters.keys()]
        return ",".join(reporter_values) + "\n"

    def tick(self):
        self.ticks += 1
        if self.ticks % self.interval == 0:
            self.write()

    def newrun(self):
        self.run += 1
        self.ticks = 0

    def write_to_file(self, line, method='a', file=None, file_open=False):
        if file is None:
            file = self.outfile
        if file_open:
            file.write(line)
        else:
            with open(file, method) as f:
                f.write(line)


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