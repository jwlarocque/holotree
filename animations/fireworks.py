import time
import math
import random
import colorsys

import numpy as np
from scipy.spatial.distance import cdist


ID = "fireworks"
CENTER = (0, 0, 1)
ROCKET_RADIUS = 0.2
MAX_HORIZ_LAUNCH_VELOCITY = 0.25
MAX_VERT_LAUNCH_VELOCITY = 2.2
MIN_VERT_LAUNCH_VELOCITY = 1.9
GRAVITY = np.array([0., 0., -1])

class FrameGenerator():
    debug = True

    def __init__(self, lights: np.ndarray):
        """
        Args:
            A numpy ndarray of shape (~1000, 3) giving the x, y, z coordinates
            of each light on the tree.
        """
        self.lights = lights
        self.reset_firework()
        self.last_frame_time = None

    def reset_firework(self):
        self.detonated = False
        vx = (2 * random.random() - 1) * MAX_HORIZ_LAUNCH_VELOCITY
        vy = (2 * random.random() - 1) * MAX_HORIZ_LAUNCH_VELOCITY
        vz = random.random() * (MAX_VERT_LAUNCH_VELOCITY - MIN_VERT_LAUNCH_VELOCITY) + MIN_VERT_LAUNCH_VELOCITY
        self.pos = np.array([0., 0., 0.])
        self.velocity = np.array([vx, vy, vz])
        self.color = colorsys.hsv_to_rgb(random.random(), 1, 1)
        self.detonation_time = None
        self.expansion_rate = None
        self.explosion_radius = 0.3
        self.brightness = 1.0

    def toggle_debug(self):
        """
        Toggle debug mode (simulator only). Do whatever you want with this.
        """
        self.debug = not self.debug

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
        if self.last_frame_time is None:
            self.last_frame_time = this_frame_time - 1e-2
        delta = (this_frame_time - self.last_frame_time)
        # update firework position and velocity
        self.pos += self.velocity * delta
        self.velocity += GRAVITY * delta
        if self.detonated:
            self.velocity -= 5 * self.velocity * delta
            self.explosion_radius += self.expansion_rate * delta
            self.expansion_rate -= 1 * self.expansion_rate * (this_frame_time - self.detonation_time)
            self.expansion_rate = max(self.expansion_rate, 0)
            self.brightness = max(0, self.brightness * (1 - 0.005 * (this_frame_time - self.detonation_time)))
            if self.brightness < 0.01:
                self.reset_firework()
        if self.pos[2] < -1 * (self.explosion_radius or ROCKET_RADIUS):
            self.reset_firework()
        # decide whether to detonate; probability goes up as the firework begins to fall
        if not self.detonated:
            if random.random() < (0.01 + -.03 * self.velocity[2]) / delta:
                self.detonated = True
                self.detonation_time = this_frame_time
                self.expansion_rate = (random.random() + 0.5) * 3
                self.velocity *= 0.5

        self.last_frame_time = this_frame_time

        firework_dists = cdist(self.lights, [self.pos])
        colors = []
        for i in range(len(self.lights)):
            if self.detonated:
                if firework_dists[i] < self.explosion_radius:
                    colors.append(tuple(val * self.brightness for val in self.color))
                else:
                    colors.append((0, 0, 0))
            elif firework_dists[i] < ROCKET_RADIUS:
                colors.append((1, 0.6, 0))
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
