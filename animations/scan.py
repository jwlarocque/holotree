import time

import numpy as np


ID = "scan"

RADIANCE_DIST = 0.4
BOUNDS = [(-1, 1), (-1, 1), (0, 3)]
COLORS = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

class FrameGenerator():
    def __init__(self, lights: np.ndarray):
        """
        Args:
            A numpy ndarray of shape (~1000, 3) giving the x, y, z coordinates
            of each light on the tree.
        """
        self.lights = lights
        self.start_time = time.time()

    def toggle_debug(self):
        pass

    def get_debug_objects(self):
        return []
    
    def get_frame(self):
        curr_time = (time.time() - self.start_time) / 1.5
        axis = int(curr_time / 2) % 3
        direction = int(curr_time) % 2
        curr_min = BOUNDS[axis][0] - RADIANCE_DIST
        curr_max = BOUNDS[axis][1] + RADIANCE_DIST
        if direction == 0:
            curr_max, curr_min = curr_min, curr_max
        pos = (curr_max - curr_min) * (curr_time % 1) + curr_min

        colors = []
        for light in self.lights:
            dist = abs(light[axis] - pos)
            colors.append(COLORS[axis] * radiance_decay_func(dist))
        return colors

def radiance_decay_func(x):
    return 1 / (1 + (x / .05) ** 2.5)