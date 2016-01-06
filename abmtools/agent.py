
import copy

a_ident = 0


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
