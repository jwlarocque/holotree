# within shells interlinked
import time
import math

import numpy as np


CENTER = (0, 0, 1)

NUM_SECTIONS = 4
ID = "dad"

class FrameGenerator():
    
    # origin = vedo.Point(pos=(0, 0, 0)) # for debug purposes
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
        this_frame_time = time.time() / 4

        colors = []
        for light in self.lights:
            theta = (math.atan2(light[1], light[0]) / math.pi + 1) / 2
            min_bound = this_frame_time % 1
            max_bound = (this_frame_time % 1 + 0.5) % 1
            # min_bounds = [(bound / NUM_SECTIONS + this_frame_time) % 1 for bound in range(0, NUM_SECTIONS)]
            # max_bounds = [bound + 1 / NUM_SECTIONS for bound in min_bounds]
            # in_section = True
            # for i in range(0, len(min_bounds), 2):
            #     min_bound = min_bounds[i]
            #     max_bound = max_bounds[i]
            #     if (theta > min_bound and theta < max_bound) or (min_bound > max_bound and (theta > min_bound or theta < max_bound)):
            #         break
            #     else:
            #         in_section = False
            # if in_section:
            #     colors.append((1, 0, 0))
            # else:
            #     colors.append((1, 1, 1))
            theta = (theta + 0.5 * light[2]) % 1
            if (theta > min_bound and theta < max_bound) or (min_bound > max_bound and (theta > min_bound or theta < max_bound)):
                colors.append((.2, 0, 0))
            else:
                colors.append((.05, .05, .05))
        return colors
    
    def get_debug_objects(self):
        """
        Returns:
            A list of vedo objects to be rendered in the simulator.
        """
        return []

def point_dist(p1, p2):
    return math.sqrt(np.sum((np.array(p2) - np.array(p1)) ** 2))
