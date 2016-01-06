# ABMtools

*This package is sort of ready to use. A lot of the intended functionality is there. However, all of it might be redesigned in the future, and changes will likely not be backwards-compatible.*

## Goals and non-goals
The goal of this project is to avoid having to write the same things over and over for each Agent-Based Model you create. Every model tends to need agents, groups, some global element to control and keep track of these agents and groups, and supporting functions which are frequently used.
This package is meant to provide base cases for these classes and functions, with enough functionality that the only additions you have to write yourself will be functionality specific to the model you are writing.

### Stuff that should be in a final version
1. Prototype agents and groups to use in your models.
2. Classes and functions to set up and run a model.
3. Connections between agents and groups
4. Ability to create a grid-based world and functions to make managing this world easier
5. Ability to simulate multiple runs of the model in parallel

### Stuff that shouldn't be in a final version
1. Real-time visualization. This is not NetLogo and doesn't want to be (although I take some inspiration from it here and there, e.g. in how functions are named).
2. GUI. This will be a script-only package. You will not be able to start, stop or control your simulations through a graphical interface unless you design one yourself.
3. Analysis tools. This package should be light-weight, with few dependencies outside of the Python 3 standard library. The best assistance this package can give to aid analysis is to output results in a way which established analysis tools (e.g. Matplotlib & pandas for Python, or other software like R) can read.

In the ideal case this package and its dependencies should be reliably installable everywhere through a single command: `pip install abmtools`. This may not be entirely feasible, given that a package like Numpy (notoriously difficult to install through pip in a regular Python 3 environment on Windows) might prove necessary to make some parts of the package work efficiently. 
 In those cases parts of the package may be made optional.