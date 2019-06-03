
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
            self.write_to_file(self.header(), method='w+')
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
