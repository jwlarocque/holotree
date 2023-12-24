import time
import math

import numpy as np
from scipy.spatial.distance import cdist


ID = "snow"
RADIUS = 1
HEIGHT = 3
NUM_FLAKES = 5

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
        self.flake_heights = np.linspace(HEIGHT, HEIGHT * 2 + 1, NUM_FLAKES) #np.random.rand(NUM_FLAKES) * HEIGHT + HEIGHT
        self.flake_horiz = np.random.rand(NUM_FLAKES) * RADIUS
        alphas = 2 * math.pi * np.random.rand(NUM_FLAKES)
        radii = np.random.rand(NUM_FLAKES) * RADIUS # TODO: consider sqrt of rand for equal distribution
        self.flake_xs = radii * np.cos(alphas)
        self.flake_ys = radii * np.sin(alphas)

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
        if not self.last_frame_time:
            self.last_frame_time = time.time()
        delta = (time.time() - self.last_frame_time) * .3
        self.last_frame_time = time.time()

        for i in range(NUM_FLAKES):
            self.flake_heights[i] -= delta
            if self.flake_heights[i] < -0.5:
                self.flake_heights[i] = HEIGHT + 0.5
                # randomize position of flake i
                self.flake_xs[i] = np.random.rand() * RADIUS * np.cos(2 * math.pi * np.random.rand())
                self.flake_ys[i] = np.random.rand() * RADIUS * np.sin(2 * math.pi * np.random.rand())

        colors = []
        min_dists = np.min(cdist(self.lights, np.array([self.flake_xs, self.flake_ys, self.flake_heights]).transpose()), axis=1)
        for i in range(len(self.lights)):
            radiance = radiance_decay_func(min_dists[i])
            if radiance > 0.1:
                colors.append((radiance*1, radiance*1, radiance*0.7))
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

def radiance_decay_func(x):
    return 1 / (1 + (x / .1) ** 3)
