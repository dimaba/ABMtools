
from abmtools import agent

g_ident = 0


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
            agents.append(agent.Agent(controller=self.controller, group=self.ident, *args, **kwargs))

        self.members += agents
        self.controller.agents += agents
        self.update_size()
