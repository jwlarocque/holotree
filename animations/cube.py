import time

import numpy as np
from scipy.spatial.transform import Rotation


# For use with the actual tree, do not alter the name of `FrameGenerator` or the
# signature of the `__init__` and `get_frame` functions.
# NOTE: You can use Vedo objects for geometry (it's handy for viewing them
#       in the "simulator"), but you don't have to.
# NOTE: The tree in the simulator has a base radius of 1 and a height of 3.
#       This may approximate the shape of the real tree but you may want to
#       write something to examine the actual positions of the lights passed
#       in to make positioning decisions. Otherwise please pull out some consts
#       like CUBE_HEIGHT below to make repositioning easy.
#       (Regardless of shape, the origin on the real tree will be in the same
#        place as in the simulator - centered at the base of the branches, and
#        the radius at the widest point will be 1.)

ENABLED = False
CUBE_HEIGHT = 1.2

class FrameGenerator():
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]) * 1.3
    vertices = vertices / 2.5 + [0, 0, CUBE_HEIGHT] # fit inside tree
    cube_edges = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
        [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]])
    last_frame_time = time.time()
    # debug = True
    rot = Rotation.from_euler("xyz", [45, 45, 0], degrees=True)
    for  i in range(len(vertices)):
        vertices[i] = rot.apply(vertices[i] - [0, 0, CUBE_HEIGHT]) + [0, 0, CUBE_HEIGHT]

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
        # self.debug = not self.debug
        # if self.debug:
        #     self.cube.wireframe(True)
        #     self.cube.alpha = 1.0
        #     self.origin.alpha(1.0)
        # else:
        #     self.cube.wireframe(False)
        #     self.cube.alpha = 0.0
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
        this_frame_time = time.time()
        delta = (this_frame_time - self.last_frame_time) * 20
        self.last_frame_time = this_frame_time

        rot = Rotation.from_euler("xyz", [0, 0, delta], degrees=True)
        for  i in range(len(self.vertices)):
            self.vertices[i] = rot.apply(self.vertices[i] - [0, 0, CUBE_HEIGHT]) + [0, 0, CUBE_HEIGHT]
        # self.cube.rotate_x(delta * 5, around=[0, 0, CUBE_HEIGHT])
        # self.cube.rotate_y(delta * 5, around=[0, 0, CUBE_HEIGHT])
        # self.cube.rotate_z(delta * 5, around=[0, 0, CUBE_HEIGHT])

        min_dists = None
        for edge in self.vertices[self.cube_edges]:
            dists = lineseg_dists(self.lights, edge[0], edge[1])
            if min_dists is None:
                min_dists = dists
            else:
                min_dists = np.minimum(min_dists, dists)

        colors = []
        for i in range(len(min_dists)):
            brightness = radiance_decay_func(min_dists[i])
            colors.append((brightness, brightness, brightness))

        return colors
    
    def get_debug_objects(self):
        """
        Returns:
            A list of vedo objects to be rendered in the simulator.
        """
        return []

def rotateMatrix(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]) + []

def radiance_decay_func(x):
    return 1 / (1 + (x / .02) ** 3)

def lineseg_dists(p, a, b):
    # adapted from https://stackoverflow.com/questions/54442057/calculate-the-euclidian-distance-between-an-array-of-points-to-a-line-segment-in/54442561#54442561
    p = np.atleast_2d(p)
    if np.all(a == b):
        return np.linalg.norm(p - a, axis=1)
    d = np.divide(b - a, np.linalg.norm(b - a))
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)
    h = np.maximum.reduce([s, t, np.zeros(len(p))])
    c = np.cross(p - a, d)
    return np.hypot(h, (c * c).sum(axis=1))
