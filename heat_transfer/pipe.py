import numpy as np

from heat_transfer.dynamic_object import DynamicObject
from heat_transfer.flow_object import FlowObject


class Pipe(FlowObject, DynamicObject):
    """
    Describes an ideal pipe between two stacks.
    There is no friction in the pipe, and we assume that the pipe's radius is small enough such that there is no
    radial temperature gradient.
    """

    def rhs_temperature(self, setup):
        """
        return temperature of the pipe's surrounding
        :param setup: environment setup
        :return: value of the temperature of the external environment
        """
        return setup.T_env

    def time_step(self, setup):
        """
        solve next step of the partial differential equation:
          ∂T/∂t = a ∂T/∂x + b(T_env - T)
        using finite differences implicit scheme.
        :param setup: environment setup
        """
        if self._T_inlet is None:
            raise RuntimeError("Pipe is not connected to a source.")
        area = 2 * np.pi * self._radius * self._dl
        volume = self._dl * np.pi * self._radius ** 2
        temperature = np.zeros(self._n + 2)
        a = self.flow_rate / (setup.rho * np.pi * self._radius ** 2)
        b = self._dt * self._heat_transfer * area / (setup.rho * setup.Cp * volume)
        external_temperature = self.rhs_temperature(setup)
        temperature[1:-1] = self._T[:] + external_temperature * b
        temperature[0] = self.T_inlet + external_temperature * b
        temperature[-1] = 0
        # fill matrix for implicit scheme solution
        A = np.zeros((self._n + 2, self._n + 2))
        A[0, 0] = 1.0 + b
        for i in range(1, self._n + 1):
            A[i, i - 1] = -a * self._dt / self._dl
            A[i, i] = 1.0 + a * self._dt / self._dl + b
        A[-1, -1] = 1.0 + b
        self._T[:] = np.linalg.solve(A, temperature)[1:-1]

    def __init__(self, length: float = 50, n: int = 500, u: float = 0.0, **params):
        """
        :param temp_init: initial temperature inside the pipe
        :param length: length of the pipe
        :param radius: radius of the pipe
        """
        FlowObject.__init__(self, temp_init=params["temp_init"])
        DynamicObject.__init__(self, dt=params["dt"], t_max=params["t_max"])
        self.title = "Pipe"
        self._length = length
        self._radius = params["port_radius"]
        self._heat_transfer = u
        self._n = n  # number of discretization steps
        self._dl = self._length / n  # discretization step along the pipe
        self._x = np.linspace(self._dl / 2, self._length - self._dl / 2, n)  # center of each elementary cell
        self._T = np.ones(n) * self.T_init  # initial temperature inside the pipe
        self._dTdt = np.zeros(n)  # initialize temperature change rate to zero
        self._ax = None

    def update(self):
        super().update()
        self._T_outlet = self._T[-1]

    @property
    def length(self):
        return self._length

    @property
    def radius(self):
        return self._radius

    @property
    def temperature(self):
        return self._T

    def print(self):
        super().print()
        if self._ax is not None:
            self._ax.cla()
            y = np.tile(self._T, (self._T.shape[0] // 10, 1))
            self._ax.title.set_text(self.title)
            self._ax.imshow(y, cmap="plasma", vmin=self._ax.v_min, vmax=self._ax.v_max, aspect="equal")
