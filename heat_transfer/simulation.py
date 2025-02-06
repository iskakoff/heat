from argparse import Namespace

import matplotlib.pyplot as plt
from matplotlib import cm, colors

from heat_transfer.flow_object import FlowObject
from heat_transfer.pump import Pump


class Simulation(object):
    """
    Class to control the heat transfer simulation.
    """

    def __init__(self, objects: list[FlowObject], **setup):
        self.pump = None
        # setup visualization
        # since Pump is a point object and there is no flow through it, there is nothing to be visualized
        count = 0
        for i, obj in enumerate(objects):
            if isinstance(obj, Pump):
                continue
            count += 1
        fig, axs = plt.subplots(count, 1, layout='constrained', figsize=(10, 8))
        v_max = max(setup["T_env"], setup["temp_init"], setup["steady_temperature"]) + 20
        v_min = min(setup["T_env"], setup["temp_init"], setup["steady_temperature"]) - 20

        fig.colorbar(cm.ScalarMappable(norm=colors.Normalize(v_min, v_max), cmap=cm.get_cmap("plasma")), ax=axs[0])
        plt.xlim(100)
        count = 0
        for i, obj in enumerate(objects):
            if not isinstance(obj, Pump):
                obj._ax = axs[count]
                obj._ax.v_min = v_min
                obj._ax.v_max = v_max
                count += 1

        # find pump object
        for i, obj in enumerate(objects):
            if isinstance(obj, Pump) and self.pump is None:
                self.pump = obj
            elif isinstance(obj, Pump) and self.pump is not None:
                raise RuntimeError("Only single pump allowed.")

        # connect all objects together
        current = objects[0]
        for i, obj in enumerate(objects[1:]):
            # attach the outlet port of the current object into the inlet port of the next object in list
            current.attach(obj)
            current = obj
        if self.pump is None:
            raise RuntimeError("No pump attached.")
        current.attach(objects[0])
        self._root = objects[0]
        self._objects = objects
        self._setup = Namespace(**setup)
        # update flow rate in all objects
        obj = self.pump.outlet
        while not isinstance(obj, Pump) and obj.outlet is not None:
            obj.update()
            obj = obj.outlet

    def update(self, iter: int):
        """
        Iterate over the objects and update the heat transfer state (we need to match outlet an inlet temperatures along the fluid flow).
        """
        obj = self.pump.outlet
        while not isinstance(obj, Pump) and obj.outlet is not None:
            obj.update()
            if iter % 2 == 0:
                obj.print()
            obj = obj.outlet
            plt.pause(0.1)
        self.pump.update()

    def simulate(self):
        """
        Simulate the heat transfer for the given number of time steps.
        """
        for i in range(self._setup.t_max):
            if i % 20 == 0:
                print(f"Iteration {i} out of {self._setup.t_max}")
            self.update(i)
            self._root.time_step(self._setup)
            obj = self._root.outlet
            while obj is not self._root:
                obj.time_step(self._setup)
                obj = obj.outlet
        plt.show()
