# within shells interlinked
import time
import math

import numpy as np

ID = "mom"
CENTER = (0, 0, 1)

class FrameGenerator():
    debug = True

    def __init__(self, lights: np.ndarray):
        """
        Args:
            A numpy ndarray of shape (~1000, 3) giving the x, y, z coordinates
            of each light on the tree.
        """
        self.lights = lights

    def toggle_debug(self):
        """
        Toggle debug mode (simulator only). Do whatever you want with this.
        """
        self.debug = not self.debug

    def get_car_pos(self, this_frame_time):
        car_z = (this_frame_time / 4) % 3
        car_x = 0.8 * math.sin(5 * this_frame_time) * (1 - (car_z / 3))
        car_y = 0.8 * math.cos(5 * this_frame_time) * (1 - (car_z / 3))
        return (car_x, car_y, car_z)

    def get_frame(self):
        """
        Generate a frame for the tree animation.
        
        Returns:
            A list or numpy ndarray of (r, g, b) values for each light. The
            length of the list must be equal to the length of self.lights, and
            each value must be between 0 and 1.
            Optionally, for simulation purposes, you can return a list of
            (r, g, b, a) values for each light (for instance, to hide non-
            illuminated lights). The alpha values will be *discarded* by the
            actual tree.
        """
        this_frame_time = time.time()
        car_1_coords = self.get_car_pos(this_frame_time)
        bus_coords = self.get_car_pos(this_frame_time / 2)
        colors = []
        for light in self.lights:
            dist_from_car = point_dist(light, car_1_coords)
            dist_from_bus = point_dist(light, bus_coords)
            if dist_from_car < .2:
                colors.append((1, 0, 0))
            elif dist_from_bus < .2:
                colors.append((1, 1, 0))
            else:
                colors.append((0, 0, 0))
        return colors
    
    def get_debug_objects(self):
        """
        Returns:
            A list of vedo objects to be rendered in the simulator.
        """
        return []

def point_dist(p1, p2):
    return np.linalg.norm(p2 - p1)
