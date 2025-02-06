import argparse

from heat_transfer.pipe import Pipe
from heat_transfer.pump import Pump
from heat_transfer.simulation import Simulation
from heat_transfer.solar import Solar
from heat_transfer.tank import Tank


def main():
    parser = argparse.ArgumentParser()
    # simulation parameters
    parser.add_argument("--Cp", default=4180.0, type=float, help="heat capacity")
    parser.add_argument("--rho", default=1000.0, type=float, help="fluid density")
    parser.add_argument("--T_env", default=280, type=float, help="environment temperature")
    parser.add_argument("--port_radius", default=0.1, type=float, help="radius of pipes in the simulation")
    parser.add_argument("--dt", default=1, type=float, help="time discretization step")
    parser.add_argument("--t_max", default=800, type=int, help="number of time steps")
    parser.add_argument("--steady_temperature", default=600, type=float, help="internal temperature of the solar panel")
    parser.add_argument("--temp_init", default=400, type=float, help="initial temperature of the liquid in the system")
    parser.add_argument("--flow_rate", default=20, type=float, help="flow rate in the pump")

    args = parser.parse_args()
    v = vars(args)

    """
    The task is to simulate the behaviour of the system below 
    
    
        Solar
Sun     panel
light   ______   Pipe 1    Pump   Pipe 2    ______________
    --> |    | ══════════════O══════════════|            |
    --> |    |                              |            |
        |    | ════════════════╗            |    Tank    |
        ¯¯¯¯¯¯    Pipe 3       ║            |            |
                               ║            |            |
                               ╚════════════|            |
                                            ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    """

    # initialize objects used in the simulation
    solar = Solar(**v)
    pipe_1 = Pipe(length=0.3, u=1000, n=20, **v)
    pipe_2 = Pipe(length=0.3, u=1000, n=20, **v)
    tank = Tank(tank_radius=0.2, tank_length=50, nx=30, ny=100, **v)
    pipe_3 = Pipe(length=0.3, u=1000, n=20, **v)
    pump = Pump(args.flow_rate, args.temp_init)

    sim = Simulation([solar, pipe_1, pump, pipe_2, tank, pipe_3], **vars(args))
    sim.simulate()


if __name__ == '__main__':
    main()
