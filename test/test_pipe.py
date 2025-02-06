import unittest
from types import SimpleNamespace

from heat_transfer import pipe
from heat_transfer.constant_t_source import ConstantTSource


class PipeTestCase(unittest.TestCase):
    def test_init(self):
        p = pipe.Pipe(temp_init=100, length=10, port_radius=0.2, n=50, dt=0.1, t_max=100)
        self.assertEqual(p.T_init, 100)
        self.assertEqual(p.length, 10)
        self.assertEqual(p.radius, 0.2)
        self.assertEqual(p.dt, 0.1)
        self.assertEqual(p.t_max, 100)

    def test_attach(self):
        p1 = pipe.Pipe(temp_init=100, length=10, port_radius=0.2, n=50, dt=0.1, t_max=100)
        p2 = pipe.Pipe(temp_init=100, length=10, port_radius=0.2, n=50, dt=0.1, t_max=100)
        p1.attach(p2)
        self.assertEqual(p1.outlet, p2)
        self.assertEqual(p2.inlet, p1)

    def test_time_step_unattached(self):
        p = pipe.Pipe(temp_init=100, length=10, port_radius=0.2, n=10, dt=0.1, t_max=100)
        self.assertRaises(RuntimeError, p.time_step, self.setup)

    def test_time_step(self):
        source = ConstantTSource(temp_init=100)
        p = pipe.Pipe(temp_init=100, length=10, port_radius=0.2, n=10, dt=0.1, t_max=100)
        source.attach(p)
        T_out_init = p.temperature[-1]
        p.time_step(self.setup)
        T_out = p.temperature[-1]
        self.assertEqual(T_out_init, T_out)

        # Test that pipe with non-zero heat_transfer transfer coefficient will lose temperature to the environment
        p2 = pipe.Pipe(temp_init=150, length=10, port_radius=0.2, n=10, dt=0.1, t_max=100, u=0.01)
        source.attach(p2)
        T_out_init = p2.temperature[-1]
        p2.time_step(self.setup)
        T_out = p2.temperature[-1]
        self.assertGreater(T_out_init, T_out)

        # Test that pipe with non-zero heat_transfer transfer coefficient will absorb temperature to the environment
        p3 = pipe.Pipe(temp_init=50, length=10, port_radius=0.2, n=10, dt=0.1, t_max=100, u=0.01)
        source.attach(p3)
        T_out_init = p3.temperature[-1]
        p3.time_step(self.setup)
        T_out = p3.temperature[-1]
        self.assertLess(T_out_init, T_out)

    def setUp(self):
        """
        Initialize test setup environment
        """
        setup = SimpleNamespace()
        setup.Cp = 1.0
        setup.rho = 1.0
        setup.T_env = 100
        setup.port_radius = 0.1
        self.setup = setup


if __name__ == '__main__':
    unittest.main()
