from abc import ABC, abstractmethod


class DynamicObject(ABC):
    """
    Describes a general interface for objects that depend on time.
    """

    def __init__(self, dt: float, t_max: int):
        """
        :param dt : step in time
        :param t_max : maximum time steps to simulate
        """
        self._dt = dt
        self._t_max = t_max

    @abstractmethod
    def time_step(self, setup):
        """
        Update object state for the next time step.
        :param setup: simulation setup
        """
        pass

    @property
    def dt(self):
        return self._dt

    @property
    def t_max(self):
        return self._t_max
