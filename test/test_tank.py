import unittest
from types import SimpleNamespace

from heat_transfer.constant_t_source import ConstantTSource
from heat_transfer.tank import Tank


class TankTestCase(unittest.TestCase):
    def test_tank_init(self):
        t = Tank(10, 10, 10, 10, temp_init=100, **vars(self.setup))
        s = ConstantTSource(temp_init=500)
        s.attach(t)
        t.time_step(self.setup)
        t.update()
        self.assertGreater(t.temperature[0], t.temperature[1])

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
