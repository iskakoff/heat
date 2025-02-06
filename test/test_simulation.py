import unittest
from types import SimpleNamespace

from heat_transfer.pipe import Pipe
from heat_transfer.pump import Pump
from heat_transfer.simulation import Simulation


class MyTestCase(unittest.TestCase):
    def test_simulation_setup(self):
        objects = [Pipe(**vars(self.setup)), Pump(self.setup.flow_rate, self.setup.temp_init), Pipe(**vars(self.setup))]
        s = Simulation(objects, **vars(self.setup))
        for i, o in enumerate(objects[:-1]):
            self.assertEqual(o.outlet, objects[i + 1])
        self.assertEqual(objects[-1].outlet, objects[0])

    def test_simulation_setup_no_pump(self):
        objects = [Pipe(**vars(self.setup)), Pipe(**vars(self.setup))]
        self.assertRaises(RuntimeError, lambda: Simulation(objects, **vars(self.setup)))

    def setUp(self):
        self.setup = SimpleNamespace()
        # liquid parameters
        self.setup.Cp = 1.0
        self.setup.rho = 1.0
        # environment
        self.setup.T_env = 100
        self.setup.steady_temperature = 100
        # objects parameters
        self.setup.port_radius = 0.1
        self.setup.temp_init = 10.0
        self.setup.flow_rate = 10.0

        # simulation parameters
        self.setup.dt = 0.1
        self.setup.t_max = 100


if __name__ == '__main__':
    unittest.main()
