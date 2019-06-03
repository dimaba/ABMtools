# ABMtools

*This package is sort of ready to use. A lot of the intended functionality is there. However, all of it might be redesigned in the future, and changes will likely not be backwards-compatible.*

## Installation and testing instructions
To quickly install and try some of the examples in this package, the following steps are recommended:
- Clone or download the package directly from this page
- (Optional but recommended:) Create and activate a virtual environment in which to install the package with an up to date version of Python 3
- Navigate to the ABMtools directory in your system terminal
- Run `python setup.py` to install the package locally
You should then be able to run any of the tests and examples in the Tests directory, as long as your virtual environment is activated and you navigate to the Tests directory. To visualize the results from the Bowles and Gintis (2004) example you can use `plot_results.py` in the Results directory, if `matplotlib` is installed in your virtual environment.

This package is not currently available on package indexes such as PyPi.

## Goals and non-goals
The goal of this project is to avoid having to write the same things over and over for each Agent-Based Model you create. Every model tends to need agents, groups, some global element to control and keep track of these agents and groups, and supporting functions which are frequently used.
This package is meant to provide base cases for these classes and functions, with enough functionality that the only additions you have to write yourself will be functionality specific to the model you are writing.
The package is based on the available functionality of NetLogo. NetLogo is easy to work with and has nice integrated visualization options, but it is also very slow and somewhat restrictive. 

### Stuff that should be in a final version
1. Prototype agents and groups to use in your models (Complete)
2. Classes and functions to set up and run a model (Complete)
3. Connections between agents and groups (Incomplete)
4. Ability to create a grid-based world and functions to make managing this world easier (Not implemented)
5. Ability to simulate multiple runs of the model in parallel (Incomplete)

### Stuff that shouldn't be in a final version
1. Real-time visualization. This is not NetLogo and doesn't want to be (although I take some inspiration from it here and there, e.g. in how functions are named).
2. GUI. This will be a script-only package. You will not be able to start, stop or control your simulations through a graphical interface unless you design one yourself.
3. Analysis tools. This package should be light-weight, with few dependencies outside of the Python 3 standard library. The best assistance this package can give to aid analysis is to output results in a way which established analysis tools (e.g. Matplotlib & pandas for Python, or other software like R) can read.

In the ideal case this package and its dependencies should be reliably installable everywhere through a single command: `pip install abmtools`. This may not be entirely feasible, given that a package like Numpy (notoriously difficult to install through pip in a regular Python 3 environment on Windows) might prove necessary to make some parts of the package work efficiently. 
 In those cases parts of the package may be made optional.
