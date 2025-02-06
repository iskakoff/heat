from heat_transfer.flow_object import FlowObject


class ConstantTSource(FlowObject):
    """
    Source of the constant temperature flow
    """

    def time_step(self, setup):
        pass

    def __init__(self, source_flow_rate=1.0, **params):
        super(ConstantTSource, self).__init__(**params)
        self._T_outlet = params["temp_init"]
        self._flow_rate = source_flow_rate

    @property
    def flow_rate(self):
        return self._flow_rate
