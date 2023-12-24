import time
import math

import numpy as np
from scipy.spatial.distance import cdist


ID = "twinkle"
CYCLE_LENGTH = 600
FADE_DURATION = 2

class FrameGenerator():
    debug = True

    def __init__(self, lights: np.ndarray):
        """
        Args:
            A numpy ndarray of shape (~1000, 3) giving the x, y, z coordinates
            of each light on the tree.
        """
        self.last_frame_time = None
        self.lights = lights
        self.offsets = np.random.rand(len(lights)) * CYCLE_LENGTH

    def toggle_debug(self):
        """
        Toggle debug mode (simulator only). Do whatever you want with this.
        """
        self.debug = not self.debug
        # if self.debug:
        #     self.origin.alpha(1.0)
        # else:
        #     self.origin.alpha(0.0)

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
        curr_time = time.time()
        colors = []

        for i in range(len(self.lights)):
            brightness = 1 - twinkle_fade_func(curr_time + self.offsets[i])
            colors.append((brightness, brightness, 0.9 * brightness + 0.01))
        return colors
    
    def get_debug_objects(self):
        """
        Returns:
            A list of vedo objects to be rendered in the simulator.
        """
        return []

def twinkle_fade_func(x):
    fade_position = min(abs(((x + FADE_DURATION) % CYCLE_LENGTH) - FADE_DURATION) / FADE_DURATION, 1)
    return (1 - math.cos(fade_position * math.pi)) / 2