
import copy


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


def compile_typeset(individuals=None, iterables=None, instancetype=None):
    """

    Compiles individual instances and iterables of a specified type into one list of instances. Filters out anything
    included in the input which is not of the specified type.

    Args:
    :param individuals=None (iterable): A single iterable of individual instances
    :param iterables=None (iterable of iterables): An iterable which itself holds iterables of individaul instances.
        This is the way to compile multiple lists of instances
    :param instancetype=None (Class): Type of instance to include in the final typeset. The function checks for each
        instance whether it an instance of the specified Class or any of its subclasses. If None the typeset remains 
        empty


    :return:
    """

    typeset = []
    if individuals is not None:
        for i in individuals:
            if instancetype is not None and isinstance(i, instancetype):
                typeset.append(i)
    if iterables is not None:
        for s in iterables:
            for i in s:
                if instancetype is not None and isinstance(i, instancetype):
                    typeset.append(i)

    return typeset
