import time
import math

import numpy as np
from scipy.spatial.distance import cdist


ID = "snowman"
LARGE_ORB_CENTER = np.array([0.0, 0.0, 1.0])
LARGE_ORB_RADIUS = 0.8
SMALL_ORB_CENTER = np.array([0.0, 0.0, 2.1])
SMALL_ORB_RADIUS = 0.5
BODY_COLOR = (0.2, 0.2, 0.18)

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

        small_distances = cdist(self.lights, np.array([SMALL_ORB_CENTER]))
        large_distances = cdist(self.lights, np.array([LARGE_ORB_CENTER]))
        for i in range(len(self.lights)):
            if (small_distances[i] < SMALL_ORB_RADIUS
                or large_distances[i] < LARGE_ORB_RADIUS
            ):
                colors.append(BODY_COLOR)
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
