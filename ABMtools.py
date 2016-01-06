"""
EMPTY DOCSTRING
"""

import collections
import copy
a_ident = 0
g_ident = 0


class Agent:
    """

    An agent.

    This class is meant to be extended with methods specific to the ABM.
    Example: if agents in the ABM should evaluate their happiness given certain conditions,
    you would want to extend this class with a 'happiness' attribute and a method to update it.

    Args:
    :param controller (ABMTools.Controller: Controller to manage this Agent
    :param group (ABMTools.Group): Group the Agent belongs to (if any)
    :param ident (int): Agent's unique identification number

    """

    @staticmethod
    def get_ident():
        """ Get current global agent ident from ABMtools module and return it. Increment ident value for
        the next Agent."""

        global a_ident
        ident = a_ident
        a_ident += 1
        return ident

    def __init__(self, controller, group=None, ident=None):
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

        Args:
        :param register_with_group: Boolean, if True register new agent with original agent's group
        :param register_with_controller: Boolean, if True register new agent with original agent's controller

        Returns:
        :return: Return the new agent (in case you immediately want to make some modifications to new agent)

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
    """

    Group of agents.

    This class is meant to be extended with methods specific to the ABM.
    Example: if a group in the ABM should levy a tax on its members you would want to
    extend this class with a 'tax_level' attribute and a method to collect taxes.

    Args:
    :param controller (ABMtools.Controller): Controller to manage this Group
    :param ident (int): Group's unique identification number
    :param size (int): Number of members in the Group
    :param members (list of ABMtools.Agent or subclasses): All agents which are a member of this group

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
        """

        Add all members to Group.members list.

        Args:
        :param agents=None (list of ABMtools.Agent or subclasses): List of agents from which to collect members

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
        """

        Remove all members from the group. Group members are either destroyed (by removing them from their
            controller's Agent list, when kill=True) or just assigned to None group (when kill=False).

        Args:
        :param kill=False (Bool): Should agents in the group also be killed? True -> Yes, False -> No
        :param controller=None (ABMTools.Controller): Controller object which manages the group (defaults to use
                controller in self.controller when None is provided)

        """

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
        """

        Create new Agents in this group, adding them to this Group's member list.

        Args:
        :param n (int): Number of new Agents to add.
        :param args: Arguments to pass to each created Agent's init function
        :param kwargs: Keyword arguments to pass to each created Agent's init function

        """
        # Create n new agents in this group
        agents = []
        for _ in range(n):
            agents.append(Agent(controller=self.controller, group=self.ident, *args, **kwargs))

        self.members += agents
        self.controller.agents += agents
        self.update_size()

        
class Tie:
    """

    A tie between agents.

    NOT IMPLEMENTED YET

    """

    def __init__(self):
        raise NotImplementedError("ABMTools: Ties are not yet implemented")


class Controller:
    """

    A Controller. Manages Agents and Groups. Contains lists of all Agents and Groups and methods to manage their
    creation, deletion and assignment.

    This class is meant to be extended with methods specific to the ABM.
    Example: if the controller should keep track of the number of Groups or Agents with a particular attribute
    extend this class with an attribute to score the count and a method to find or calculate it.

    Args:
    :param agents=[] (list of ABMTools.Agent or subclasses): Initial list of all Agents (use if Agents have been
        created before the Controller)
    :param groups=[] list of ABMTools.Group or subclasses): Initial list of all Groups (use if Groups have been
        created before the Controller)
    :param reporters=collections.OrderedDict() (OrderedDict of 'variable name:value' pairs): Ordered dictionary of
        variables whose values should be recorded in output at every step of the simulation. Keys are variable names,
        as strings, which should correspond to attributes of the Controller object. These are read by the Ticker
        at each step of the simulation.
    :param setupvars=collections.OrderedDict() (OrderedDict of 'variable name:value' pairs): Ordered dictionary of
        variables whose values should be recorded in output at the start of the simulation. Keys are variable names,
        as strings, which should correspond to attributes of the Controller object. These are read by the Ticker
        at the start of the simulation.

    """

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
        """Update counts of Agents and Groups controlled by this Controller"""

        self.n_agents = len(self.agents)
        self.n_groups = len(self.groups)

    def create_agents(self, n=1, agenttype=Agent, agentlist='agents', *args, **kwargs):
        """

        Create Agents of a specified type (defaults to ABMTools.Agent), passing them setup arguments if necessary,
        and attach them to this Controller.

        Args:
        :param n=1 (int): Number of Agents to create
        :param agenttype=ABMTools.Agent (ABMtools.Agent or subclass thereof): Which class should be used as model for
            the created Agents
        :param agentlist='agents' (string): String name of the list of Agents the created Agents should be attached to.
            This should always be the name of an attribute of the controller. If you are using the standard
            ABMTools.Controller it can therefore only be the default value 'agents'. However, subclasses may implement
            multiple lists of Agents and this option allows you to select one of those.
        :param args: Any additional non-keyword arguments to pass to the Agents' setup function when they are created.
        :param kwargs: Any additional keyword arguments to pass to the Agent's setup function when they are created.

        """

        setattr(self, agentlist, getattr(self, agentlist) + [agenttype(self, *args, **kwargs) for _ in range(n)])
        self.update_counts()
        
    def cra(self, *args, **kwargs):
        """Shorthand for ABMTools.Controller.create_agents()"""

        self.create_agents(*args, **kwargs)
        
    def clear_agents(self, agentlist='agents'):
        """

        Remove all Agents from a list of Agents belonging to this Controller.

        Args:
        :param agentlist (string): String name of the list of Agents which should be clared.
            This should always be the name of an attribute of the controller. If you are using the standard
            ABMTools.Controller it can therefore only be the default value 'agents'. However, subclasses may implement
            multiple lists of Agents and this option allows you to select one of those.

        """

        setattr(self, agentlist, [])
        self.update_counts()
        
    def ca(self):
        """Shorthand for ABMTools.Controller.clear_agents()"""

        self.clear_agents()
        
    def create_groups(self, n=1, grouptype=Group, grouplist='groups', *args, **kwargs):
        """

        Create Groups of a specified type (defaults to ABMTools.Group), passing them setup arguments if necessary,
        and attach them to this Controller.

        Args:
        :param n=1 (int): Number of Groups to create
        :param grouptype=ABMTools.Group (ABMtools.Group or subclass thereof): Which class should be used as model for
            the created Groups
        :param grouplist='groups' (string): String name of the list of Groups the created Groups should be attached to.
            This should always be the name of an attribute of the controller. If you are using the standard
            ABMTools.Controller it can therefore only be the default value 'groups'. However, subclasses may implement
            multiple lists of Groups and this option allows you to select one of those.
        :param args: Any additional non-keyword arguments to pass to the Groups' setup function when they are created.
        :param kwargs: Any additional keyword arguments to pass to the Group's setup function when they are created.

        """

        setattr(self, grouplist, getattr(self, grouplist) + [grouptype(self, *args, **kwargs) for _ in range(n)])
        self.update_counts()

    def crg(self, *args, **kwargs):
        """Shorthand for ABMTools.Controller.create_groups()"""

        self.create_groups(*args, **kwargs)

    def clear_groups(self, kill=False):
        """

        Remove all Groups from a list of Groups belonging to this Controller. Optionally also kill any Agents which
        are members of these Groups.

        Args:
        :param grouplist (string): String name of the list of Agents which should be clared.
            This should always be the name of an attribute of the controller. If you are using the standard
            ABMTools.Controller it can therefore only be the default value 'agents'. However, subclasses may implement
            multiple lists of Agents and this option allows you to select one of those.
        :param kill (bool):  Determine whether or not to also kill Agents in Group's member list when Group is
            destroyed

        """

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
        """Shorthand for ABMTools.Controller.clear_groups()"""

        self.clear_groups(*args, **kwargs)

    def clear_ties(self):
        """NOT IMPLEMENTED YET"""
        raise NotImplementedError("ABMTools: Ties are not yet implemented")

    def cl(self):
        """Shorthand for ABMTools.Controller.clear_ties()"""
        self.clear_ties()

    def clear_all(self):
        """Shorthand for running both ABMTools.Controller.clear_groups and ABMTools.Controller.clear_agents()"""

        self.clear_groups()
        # self.clear_ties()
        self.clear_agents()

    def kill(self, agent=None,  ident=None):
        """

        Kill an Agent, by removing it from its Group and the Controller's Agent list.
        Agent can be passed to the method either as an object or by its ident. At least one of these must be
        specified. If more than one are specified the object is used.

        Args:
        :param agent=None (ABMTools.Agent): Object of Agent to be killed
        :param ident (int): Ident of Agent to be killed

        """

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

        Args:
        :param agent: agent to be moved
        :param target_group: group object to move agent to
        :param target_group_ident: ident of group to move agent to

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
        """

        Takes an ident number and returns the Agent in the Controller's list of Agents with a matching ident number.

        Args:
        :param ident (int): Ident number of the Agent
        :return (ABMTools.Agent or subclass): Agent object with matching ident number

        """

        if len([x for x in self.agents if x.ident == ident]) == 1:
            agent = next(x for x in self.agents if x.ident == ident)
        elif len([x for x in self.agents if x.ident == ident]) > 1:
            raise KeyError("More than one agent with ident {} found.".format(ident))
        else:
            raise KeyError("No agents with ident {} found.".format(ident))
        
        return agent

    def group(self, ident):
        """

        Takes an ident number and returns the Group in the Controller's list of Groups with a matching ident number.

        Args:
        :param ident (int): Ident number of the Group
        :return (ABMTools.Group or subclass): Group object with matching ident number

        """

        if len([x for x in self.groups if x.ident == ident]) == 1:
            group = next(x for x in self.groups if x.ident == ident)
        elif len([x for x in self.groups if x.ident == ident]) > 1:
            raise KeyError("More than one group with ident {} found.".format(ident))
        else:
            raise KeyError("No groups with ident {} found.".format(ident))
        
        return group

    def census(self, agents=None, groups=None):
        """

        Collect members for all Groups in a given list of Groups, from a given list of Agents. Attaches Agents whose
        group attribute is set to the member list of their Group. Updates size of all groups.

        Before collecting Agents each Group's member list is wiped. This method therefore completely repopulates each
        Group's member list.

        Args:
        :param agents=None (list): List of Agents to add to member lists. Defaults to using the Controller's own
            list of Agents when None
        :param groups=None (list): List of Groups whose member lists need to be filled. Defaults to using the
            Controller's own list of Agents when None

        """
        # Collect members for all groups
        if agents is None:
            agents = self.agents
        if groups is None:
            groups = self.groups

        for g in groups:
            g.members = []

        for a in agents:
            if a.group is not None:
                a.group.members.append(a)
                    
        for g in groups:
            g.update_size()


class Ticker:
    """

    A Ticker. The Ticker simplifies setup and stepping through the simulation, and handles writing summary variables
    to file. The Ticker has a setup function to call once at the start of the simulation, a step function to call
    once for every step of the simulation and a few functions for writing data.

    Args:
    :param controller=None (ABMTools.Controller or subclass): Controller for the simulation the Ticker is intended to
        manage (will usually be set or overwritten by the setup function and does then not have to be specified here)
    :param interval=1 (int): How often summary variables should be written to file (e.g. 1 = every step, 10 = every ten
        steps). Note that after the interval summary variables will be written to file in two consecutive steps. This
        is to allow comparison of change over time at different times in the simulation.
    :param run=1 (int): Simulation run number (useful when running multiple runs consecutively or in parallel).
    :param outfile="Results/run.txt" (string): File to store written data in.

    """

    def __init__(self, controller=None, interval=1, run=1, outfile="Results/run.txt"):

        self.run = run
        self.ticks = 0
        self.interval = interval
        self.setup_func = None
        self.step_func = None
        self.controller = controller
        self.outfile = outfile

    def set_setup(self, func, *args, **kwargs):
        """

        Set the setup function which will then be run when ABMTools.Ticker.setup() is called. The setup function must
        return an ABMTools.Controller object or subclass thereof which contains the full setup of the simulation. The
        setup function is stored as a tuple of the function and its arguments.

        Args:
        :param func (func): Function object for setup function
        :param args: Any non-keyword arguments to be passed to the setup function
        :param kwargs: Any keyword arguments to be passed to the setup function

        """

        self.setup_func = (func, args, kwargs)

    def setup(self, set_controller=True):
        """

        Runs the setup function stored as an attribute of this Ticker. By default also sets the Ticker's controller
        attribute to be the Controller returned by the setup function.

        Args:
        :param set_controller=True (bool): If True, set the Ticker's controller attribute to be the Controller returned
            by the setup function. If False, ignore

        Returns:
        :return (ABMTools.Controller or subclass): Returns Controller object created by the setup function

        """

        func = self.setup_func[0]
        args = self.setup_func[1]
        kwargs = self.setup_func[2]
        c = func(*args, **kwargs)
        if set_controller:
            self.controller = c
        return c

    def header(self):
        """Set the header for the data file including setup variable values and reporter name"""

        header = ""
        setupattr = [getattr(self.controller, var) for var in self.controller.setupvars.keys()]
        for varname, value in zip(self.controller.setupvars.values(), setupattr):
            header += ("{} = {}\n".format(varname, value))
        header += ",".join([str(k) for k in self.controller.reporters.keys()]) + "\n"
        return header

    def set_step(self, func, *args, **kwargs):
        """

        Set the step function which will then be run when ABMTools.Ticker.step() is called. The step function is stored
        as a tuple of the function and its arguments.

        Args:
        :param func (func): Function object for step function
        :param args: Any non-keyword arguments to be passed to the step function
        :param kwargs: Any keyword arguments to be passed to the step function

        """

        self.step_func = (func, args, kwargs)

    def step(self, write=True):
        """

        Runs the step function stored as an attribute of this Ticker. By default also writes summary variables
        specified as reporters in this Ticker's Controller to file.

        Args:
        :param write=True (bool): If True, write data to file (respecting the interval specified in the Ticker's
            attributes). If False, don't write date to file ever.

        """

        func = self.step_func[0]
        args = self.step_func[1]
        kwargs = self.step_func[2]
        func(*args, **kwargs)
        if write and self.ticks == 0:
            self.write_to_file(self.header(), method='w')
        if write and self.ticks % self.interval in (0, 1):
            self.write_to_file(self.report(), method='a')
        self.ticks += 1

    def report(self):
        """Generate string representation of values for all reporter variables"""

        reporter_values = [str(getattr(self.controller, var)) for var in self.controller.reporters.keys()]
        return ",".join(reporter_values) + "\n"

    def tick(self):
        """Advance ticks by one and do nothing else"""

        self.ticks += 1

    def newrun(self):
        """Set up for a new run by incrementing the run number and setting the nr of ticks to 0"""

        self.run += 1
        self.ticks = 0

    def write_to_file(self, line, method='a', file=None, file_open=False):
        """

        Writes a line to the specified data file.

        Args:
        :param line (str): Line of data or other text to be written to file
        :param method='a' (str): File writing method. Defaults to append
        :param file=None (str): File name which can be specified if you want to write to a different file from the one
            in the Ticker's outfile attribute
        :param file_open=False (bool): If you are calling this write_to_file function from a context where the
            destination file is already opened, set this to True to avoid attempting to open the file more than once

        """

        if file is None:
            file = self.outfile
        if file_open:
            file.write(line)
        else:
            with open(file, method) as f:
                f.write(line)


##############################
    
def max_one_of(agentset, var):
    """

    Find Agent with highest value of a specified variable in the specified Agentset. Returns only the first such agent
    even if multiple agents share this maximum value

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to maximize

    Returns:
    :return (ABMTools.Agent or subclass): Agent with the highest value on the specified variable

    """

    maxval = max([getattr(agent, var) for agent in agentset])
    
    return next(agent for agent in agentset if getattr(agent, var) == maxval)


def max_n_of(agentset, var, n):
    """

    Find N Agents with the highest values on a specified variable in the specified Agentset. Returns only the first N
    such Agents if there are more which share the maximum value. Returns Agents with second-highest value and so on
    if less than N Agents share the maximum value

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to maximize
    :param n (int): Number of Agents to return

    Returns:
    :return (list of ABMTools.Agent or subclass): List length N containing Agents with highest values on the specified
        variable

    """

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
    """

    Find all Agents who share the highest value of a specified variable in the specified Agentset.

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to maximize

    Returns:
    :return (list of ABMTools.Agent or subclass): List of all Agents with the highest value on the specified variable

    """

    maxval = max([getattr(agent, var) for agent in agentset])
    
    return [agent for agent in agentset if getattr(agent, var) == maxval]
    
    
def min_one_of(agentset, var):
    """

    Find Agent with lowest value of a specified variable in the specified Agentset. Returns only the first such agent
    even if multiple agents share this minimum value

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to minimize

    Returns:
    :return (ABMTools.Agent or subclass): Agent with the lowest value on the specified variable

    """

    minval = min([getattr(agent, var) for agent in agentset])
    
    return next(agent for agent in agentset if getattr(agent, var) == minval)


def min_n_of(agentset, var, n):
    """

    Find N Agents with the lowest values on a specified variable in the specified Agentset. Returns only the first N
    such Agents if there are more which share the minimum value. Returns Agents with second-lowest value and so on
    if less than N Agents share the minimum value

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to minimize
    :param n (int): Number of Agents to return

    Returns:
    :return (list of ABMTools.Agent or subclass): List length N containing Agents with lowest values on the specified
        variable

    """

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
    """

    Find all Agents who share the lowest value of a specified variable in the specified Agentset.

    Args:
    :param agentset (list of ABMTools.Agent or subclass): List of Agents within which to search
    :param var (string): Name of the variable to minimize

    Returns:
    :return (list of ABMTools.Agent or subclass): List of all Agents with the lowest value on the specified variable

    """

    minval = min([getattr(agent, var) for agent in agentset])
    
    return [agent for agent in agentset if getattr(agent, var) == minval]


def other(instance, instanceset):
    """

    Returns the same list of instances (Agents, Groups, Ties, whatever) but with one specified instance removed.

    Args:
    :param instance: Instance to remove
    :param instanceset: List of instances

    Returns:
    :return: The same list of instances, minus the one specified to be removed. To prevent accidentally removing
        instances from lists which were not intended to be modified the list returned is actually a copy of the
        input list. The input list is not modified.

    """

    new_instanceset = copy.copy(instanceset)
    new_instanceset.remove(instance)

    return instanceset


def compile_typeset(individuals=None, iterables=None, instancetype=Agent):
    """

    Compiles individual instances and iterables of a specified type into one list of instances. Filters out anything
    included in the input which is not of the specified type.

    Args:
    :param individuals (iterable): A single iterable of individual instances
    :param iterables (iterable of iterables): An iterable which itself holds iterables of individaul instances. This is
        the way to compile multiple lists of instances
    :param instancetype (Class): Type of instance to include in the final typeset. The function checks for each
        instance whether it an instance of the specified Class or any of its subclasses.


    :return:
    """

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
