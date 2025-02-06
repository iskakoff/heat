import numpy as np

from heat_transfer.dynamic_object import DynamicObject
from heat_transfer.flow_object import FlowObject


class Tank(FlowObject, DynamicObject):
    """
    Describes an ideal tank that has uniform flow distribution and no heat loss.
    """

    def time_step(self, setup):
        if self._T_inlet is None:
            raise RuntimeError("Tank is not connected to a source.")
        grad_T = (self._T[:-1] - self._T[1:]) / self._dy
        v_grad_T = grad_T * self._flow_rate
        volume = np.pi * self._dy * self._tank_radius ** 2
        self._dTdt[1:] = (setup.Cp * v_grad_T[:] * self._dy) / (setup.rho * setup.Cp * volume)
        # Boundary condition
        self._dTdt[0] = ((self.flow_rate * setup.Cp * (self._T_inlet - self._T[0])) / (setup.rho * setup.Cp * volume))
        # self._T = self._T + self._dTdt * self._dt
        T = np.zeros(self._ny + 2)
        a = self.flow_rate / (setup.rho * np.pi * self._tank_radius ** 2)
        T[1:-1] = self._T
        T[0] = self.T_inlet
        T[-1] = 0
        A = np.zeros((self._ny + 2, self._ny + 2))
        A[0, 0] = 1.0
        for i in range(1, self._ny + 1):
            A[i, i - 1] = -a * self._dt / (self._dy)
            A[i, i] = 1.0 + a * self._dt / (self._dy)
        # A[-2,-1] = -a * dt / (2 * dx)
        A[-1, -1] = 1.0
        # print(A)
        self._T[:] = np.linalg.solve(A, T)[1:-1]

    def __init__(self, tank_radius, tank_length, nx, ny, **params):
        FlowObject.__init__(self, temp_init=params["temp_init"])
        DynamicObject.__init__(self, dt=params["dt"], t_max=params["t_max"])
        self.title = "Storage tank"
        self._tank_radius = tank_radius
        self._tank_length = tank_length
        self._ny = ny
        self._dy = tank_length / ny
        self._T = np.ones(ny) * self._T_init
        self._dTdt = np.zeros(ny)
        self._ax = None

    @property
    def tank_radius(self):
        return self._tank_radius

    @property
    def tank_length(self):
        return self._tank_length

    @property
    def temperature(self):
        return self._T

    def update(self):
        super().update()
        self._T_outlet = self._T[-1]

    def print(self):
        super().print()
        if self._ax is not None:
            self._ax.cla()
            y = np.tile(self._T, (self._T.shape[0] // 5, 1))
            self._ax.title.set_text(self.title)
            self._ax.imshow(y, cmap="plasma", vmin=self._ax.v_min, vmax=self._ax.v_max, aspect="equal")
