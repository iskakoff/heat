from abc import ABC, abstractmethod
from typing import Self, Type


class FlowObject(ABC):
    """
    Class representing an abstract object that transfers fluid from an inlet to an outlet.
    """

    @abstractmethod
    def time_step(self, setup):
        pass

    @abstractmethod
    def __init__(self, temp_init: float):
        """
        Initialize the flow object with an initial temperature.
        :param temp_init: initial temperature of the fluid inside an object
        """
        self._T_init = temp_init
        self._T_inlet = None
        self._T_outlet = temp_init
        self._inlet = None
        self._outlet = None
        self._flow_rate = None

    @property
    def inlet(self):
        return self._inlet

    @property
    def outlet(self):
        return self._outlet

    @property
    def T_init(self):
        return self._T_init

    @T_init.setter
    def T_init(self, temp_init: float):
        self._T_init = temp_init

    @property
    def T_outlet(self):
        return self._T_outlet

    @T_outlet.setter
    def T_outlet(self, temp: float):
        self._T_outlet = temp

    @property
    def T_inlet(self):
        return self._T_inlet

    @T_inlet.setter
    def T_inlet(self, temp: float):
        self._T_inlet = temp

    @property
    def flow_rate(self):
        return self._flow_rate

    @flow_rate.setter
    def flow_rate(self, flow_rate: float):
        self._flow_rate = flow_rate

    def attach(self, port: Type[Self]):
        self._outlet = port
        port._inlet = self
        port.T_inlet = self._T_outlet

    def update(self):
        self._T_inlet = self._inlet.T_outlet
        self._flow_rate = self._inlet.flow_rate

    def print(self):
        pass
