import collections

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
