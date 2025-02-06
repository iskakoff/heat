import unittest
from types import SimpleNamespace

from heat_transfer.constant_t_source import ConstantTSource
from heat_transfer.solar import Solar


class SolarTestCase(unittest.TestCase):
    def test_heating(self):
        s = Solar(steady_temperature=600, temp_init=400, **vars(self.setup))
        source = ConstantTSource(temp_init=400)
        s.attach(source)
        T_out_init = s.T_outlet
        s.time_step(self.setup)
        T_out = s.temperature[-1]
        self.assertGreater(T_out, T_out_init)  # add assertion here

    def setUp(self):
        self.setup = SimpleNamespace()
        # liquid parameters
        self.setup.Cp = 1.0
        self.setup.rho = 1.0
        # environment
        self.setup.T_env = 100
        # pipes radius
        self.setup.port_radius = 0.1

        # simulation parameters
        self.setup.dt = 0.1
        self.setup.t_max = 100


if __name__ == '__main__':
    unittest.main()
