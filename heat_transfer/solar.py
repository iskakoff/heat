from heat_transfer.pipe import Pipe


class Solar(Pipe):
    """
    Describes solar panel heater behavior.
    We use the following assumptions:
      - solar panel is in thermal equilibrium state (amount of solar energy adsorbed by a panel compensate heat loss
      due to thermal conductivity and radiation)
      - heat_transfer capacity of solar panel is much larger than liquid (no temperature gradient inside the panel)
    """

    def rhs_temperature(self, setup):
        return self._steady_temperature

    def __init__(self, steady_temperature=600, heat_transfer=1000000, **params):
        Pipe.__init__(self, **params)
        self.title = "Solar panel"
        self._steady_temperature = steady_temperature
        self._heat_transfer = heat_transfer
