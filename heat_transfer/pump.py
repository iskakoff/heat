from heat_transfer.flow_object import FlowObject


class Pump(FlowObject):

    def time_step(self, setup):
        pass

    def __init__(self, flow_rate, temp_init: float):
        """
        :param flow_rate: flow rate of pump
        :param temp_init: initial temperature inside the pump
        """
        FlowObject.__init__(self, temp_init)
        self._flow_rate = flow_rate

    @property
    def flow_rate(self):
        return self._flow_rate

    @flow_rate.setter
    def flow_rate(self, value):
        self._flow_rate = value

    def attach(self, port):
        self._outlet = port
        port._inlet = self
        port.T_inlet = self._T_outlet

    def print(self):
        pass

    def update(self):
        self._T_inlet = self._inlet.T_outlet
        self._T_outlet = self._T_inlet
